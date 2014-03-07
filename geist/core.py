from __future__ import division, absolute_import, print_function

import time
import logging
from hamcrest import (
    has_length, greater_than_or_equal_to, less_than_or_equal_to)
from hamcrest.core.string_description import tostring as describe_to_string
from .keyboard import KeyDown, KeyUp, KeyDownUp, keyboard_layout_factory


logger = logging.getLogger(__name__)


class NotFoundError(LookupError):
    """Raised when something couldn't be found
    """
    pass


class Location(object):
    def __init__(self, x, y, w=0, h=0, main_point_offset=None, image=None):
        self._x, self._y, self._w, self._h = x, y, w, h
        if main_point_offset is None:
            main_point_offset = (w // 2, h // 2)
        self._main_point_offset = tuple(main_point_offset)
        self._image = image

    @property
    def image(self):
        return self._image

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def w(self):
        return self._w

    @property
    def h(self):
        return self._h

    def find(self, in_location):
        assert in_location.image is not None
        yield self.copy(
            image=in_location.image[
                self.y:self.y+self.h, self.x:self.x+self.w
            ]
        )

    def copy(self, **update_attrs):
        attrs = dict(
            (attr, getattr(self, attr)) for attr in
            ['x', 'y', 'w', 'h', 'main_point_offset', 'image']
        )
        attrs.update(update_attrs)
        return Location(attrs)

    @property
    def main_point_offset(self):
        return tuple(self._main_point_offset)

    @property
    def main_point(self):
        return (
            self.x + self._main_point_offset[0],
            self.y + self._main_point_offset[1]
        )

    @property
    def center(self):
        return (self.x + (self.w // 2), self.y + (self.h // 2))

    @property
    def rect(self):
        return (self.x, self.y, self.w, self.h)

    @property
    def area(self):
        return self.w * self.h

    def __repr__(self):
        return "Location(x=%r, y=%r, w=%r, h=%r, main_point_offset=%r)" % (
            self.x,
            self.y,
            self.w,
            self.h,
            self._main_point_offset)


class LocationList(list):
    def find(self, in_location):
        for loc in self:
            yield next(loc.find(in_location))


class GUI(object):
    def __init__(self, backend, keyboard_layout=None):
        self._backend = backend
        if keyboard_layout is None:
            keyboard_layout = keyboard_layout_factory('default')
        self._keyboard_layout = keyboard_layout
        self.config_finder_timeout = 30
        self.config_mouse_move_wait = 0.01
        self.config_mouse_button_wait = 0.01
        self.config_key_down_wait = 0.01
        self.config_key_up_wait = 0.01

    def _find_all_gen(self, finder):
        for in_location in self._backend.capture_locations():
            for loc in finder.find(in_location):
                if (in_location.x, in_location.y) != (0, 0):
                    loc = loc.copy(
                        x=loc.x + in_location.x,
                        y=loc.y + in_location.y
                    )
                yield loc

    def find_all(self, finder):
        return LocationList(finder.find(_LazyGUIMethodSnapshot(self)))

    def capture_locations(self):
        return self._backend.capture_locations()

    def wait_find_with_result_matcher(self, finder, matcher):
        start_t = time.time()
        while True:
            results = self.find_all(finder)
            if matcher.matches(results):
                return results
            if time.time() - start_t > self.config_finder_timeout:
                raise NotFoundError("Waited for results matching %s from %s."
                                    "Last result %r" % (
                                        describe_to_string(matcher),
                                        finder,
                                        results))

    def wait_find_n(self, n, finder):
        return self.wait_find_with_result_matcher(finder, has_length(n))

    def wait_find_one(self, finder):
        return self.wait_find_n(1, finder)[0]

    def click(self, finder):
        point = self.wait_find_one(finder).main_point
        # problem is numpy 32 bit ints rather than normal...
        point = (int(point[0]), int(point[1]))
        with self._backend.actions_transaction() as actions:
            actions.add_move(point)
            actions.add_wait(self.config_mouse_move_wait)
            actions.add_button_down(1)
            actions.add_wait(self.config_mouse_button_wait)
            actions.add_button_up(1)
            actions.add_wait(self.config_mouse_button_wait)

    def double_click(self, finder):
        point = self.wait_find_one(finder).main_point
        point = (int(point[0]), int(point[1]))
        with self._backend.actions_transaction() as actions:
            actions.add_move(point)
            actions.add_wait(self.config_mouse_move_wait)
            actions.add_button_down(1)
            actions.add_wait(self.config_mouse_button_wait)
            actions.add_button_up(1)
            actions.add_wait(self.config_mouse_button_wait)
            actions.add_button_down(1)
            actions.add_wait(self.config_mouse_button_wait)
            actions.add_button_up(1)
            actions.add_wait(self.config_mouse_button_wait)

    def context_click(self, finder):
        point = self.wait_find_one(finder).main_point
        point = (int(point[0]), int(point[1]))
        with self._backend.actions_transaction() as actions:
            actions.add_move(point)
            actions.add_wait(self.config_mouse_move_wait)
            actions.add_button_down(3)
            actions.add_wait(self.config_mouse_button_wait)
            actions.add_button_up(3)
            actions.add_wait(self.config_mouse_button_wait)

    def key_presses(self, *text_or_keys):
        key_actions = []
        for text_or_key in text_or_keys:
            if isinstance(text_or_key, (KeyDown, KeyUp)):
                key_actions += [text_or_key]
            elif isinstance(text_or_key, KeyDownUp):
                key_actions += [
                    KeyDown(str(text_or_key)),
                    KeyUp(str(text_or_key))
                ]
            else:
                for c in text_or_key:
                    key_actions += self._keyboard_layout(c)
        with self._backend.actions_transaction() as actions:
            for key_action in key_actions:
                if isinstance(key_action, KeyDown):
                    actions.add_key_down(str(key_action))
                    actions.add_wait(self.config_key_down_wait)
                elif isinstance(key_action, KeyUp):
                    actions.add_key_up(str(key_action))
                    actions.add_wait(self.config_key_up_wait)
                else:
                    raise ValueError('Key action must be a KeyUp or KeyDown')

    def drag(self, from_finder, to_finder):
        _from = self.wait_find_one(from_finder).main_point
        to = self.wait_find_one(to_finder).main_point
        with self._backend.actions_transaction() as actions:
            actions.add_move(_from)
            actions.add_wait(self.config_mouse_move_wait)
            actions.add_button_down(1)
            actions.add_wait(self.config_mouse_button_wait)
            actions.add_move(to)
            actions.add_wait(self.config_mouse_move_wait)
            actions.add_button_up(1)
            actions.add_wait(self.config_mouse_button_wait)

    def drag_relative(self, from_finder, offset):
        from_x, from_y = self.wait_find_one(from_finder)
        to_x, to_y = (from_x + offset[0], from_y + offset[1])
        self.drag(
            Location(from_x, from_y),
            Location(to_x, to_y)
        )

    def move(self, finder):
        point = self.wait_find_one(finder).main_point
        with self._backend.actions_transaction() as actions:
            actions.add_move(point)
            actions.add_wait(self.config_mouse_move_wait)

    def exists(self, finder):
        return True if self.find_all(finder) else False

    def exists_within_timeout(self, finder):
        try:
            self.wait_find_with_result_matcher(
                finder,
                has_length(greater_than_or_equal_to(1))
            )
            return True
        except NotFoundError:
            return False

    def does_not_exist_within_timeout(self, finder):
        try:
            self.wait_find_with_result_matcher(
                finder,
                has_length(less_than_or_equal_to(0))
            )
            return True
        except NotFoundError:
            return False

