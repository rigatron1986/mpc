import tempfile
import os

import shiboken2

import pymel.core as pm
from PySide2 import QtWidgets
from maya import OpenMayaUI as omui


def get_maya_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class TurnTableCreator(object):
    def __init__(self):
        self.turntable_path = os.path.join(tempfile.mkdtemp(), 'test.mov')
        self.group_node = 'turn_table_grp'
        self.group_offset_node = 'turn_table_offset_grp'
        self.group_height_node = 'group_height_node'
        self.group_distant_node = 'group_distant_node'
        self.lock_attrs = ['translateX', 'translateY', 'translateZ',
                           'rotateX', 'rotateY', 'rotateZ',
                           'scaleX', 'scaleY', 'scaleZ']

    def create_camera(self):
        if pm.objExists(self.group_node):
            return False
        camera_node, camera_shape = pm.camera()
        pm.viewFit(camera_shape, all=True)
        self.group_node = pm.group(empty=True, name='turn_table_grp')
        self.group_offset_node = pm.group(empty=True, name='turn_table_offset_grp')
        self.group_height_node = pm.group(empty=True, name='turn_table_height_grp')
        self.group_distant_node = pm.group(empty=True, name='turn_table_distant_grp')
        for lock_attr in self.lock_attrs:
            self.lock_attribute(self.group_node, lock_attr)
            self.lock_attribute(self.group_offset_node, lock_attr)
            self.lock_attribute(self.group_height_node, lock_attr)
            self.lock_attribute(self.group_distant_node, lock_attr)
        pm.parent(camera_node, self.group_height_node)
        pm.parent(self.group_height_node, self.group_distant_node)
        pm.parent(self.group_distant_node, self.group_offset_node)
        pm.parent(self.group_offset_node, self.group_node)
        return True

    @staticmethod
    def lock_attribute(node, attribute):
        node.setAttr(attribute, lock=True)

    @staticmethod
    def unlock_attribute(node, attribute):
        node.setAttr(attribute, lock=False)

    def delete_turn_table_group(self):
        if pm.objExists(self.group_node):
            pm.delete(self.group_node)

    def group_check(self):
        if not pm.objExists(self.group_offset_node) \
                or not pm.objExists(self.group_distant_node) \
                or not pm.objExists(self.group_height_node):
            return False
        else:
            return True

    def set_py_node(self):
        """
        Convert groups to pynode is the groups are already present.
        :return: None
        """
        self.group_offset_node = pm.PyNode(self.group_offset_node)
        self.group_distant_node = pm.PyNode(self.group_distant_node)
        self.group_height_node = pm.PyNode(self.group_height_node)

    def set_camera_position(self, attribute, value):
        """
        sets the camera depth and height
        :param attribute:
        :param value:
        :return:
        """
        if not self.group_check():
            return
        self.set_py_node()
        if attribute == 'distance':
            self.unlock_attribute(self.group_distant_node, 'translateX')
            self.unlock_attribute(self.group_distant_node, 'translateZ')
            self.group_distant_node.translateX.set(0)
            self.group_distant_node.translateZ.set(-value)
            self.lock_attribute(self.group_distant_node, 'translateX')
            self.lock_attribute(self.group_distant_node, 'translateZ')
        if attribute == 'height':
            self.unlock_attribute(self.group_height_node, 'translateX')
            self.unlock_attribute(self.group_height_node, 'translateY')
            self.group_height_node.translateX.set(0)
            self.group_height_node.translateY.set(value)
            self.lock_attribute(self.group_height_node, 'translateX')
            self.lock_attribute(self.group_height_node, 'translateY')

    def create_playblast(self, key_frames):
        """
        creates keys and generates playblast
        :param key_frames: dict of frame and key value
        :return: playblast path if success else false
        """
        if not self.group_check():
            return
        self.set_py_node()
        self.group_offset_node = pm.PyNode(self.group_offset_node)
        self.unlock_attribute(self.group_offset_node, 'rotateY')
        pm.cutKey(self.group_offset_node, attribute='rotateY', option="keys")
        for key, value in key_frames.iteritems():
            pm.setKeyframe(self.group_offset_node, attribute='rotateY', time=key, value=value, inTangentType='linear',
                           outTangentType='linear')
        self.lock_attribute(self.group_offset_node, 'rotateY')
        pm.playblast(startTime=1, endTime=key_frames + 1, format='qt', quality=100, widthHeight=[2880, 2160],
                     compression='jpeg', filename=self.turntable_path,
                     forceOverwrite=1, showOrnaments=1, clearCache=1, viewer=1, framePadding=4, percent=100)
        if os.path.exists(self.turntable_path):
            return self.turntable_path
        else:
            return False
