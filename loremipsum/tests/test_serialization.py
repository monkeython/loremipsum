"""Test serialization protocols and mediums."""

# from loremipsum import testing

import os
import tempfile


PREFIX = None


def setUpModule():
    globals()[u'PREFIX'] = tempfile.mkdtemp()


def tearDownModule():
    os.rmdir(globals()[u'PREFIX'])


# class TestSerializationMediumPkgResources(testing.TestSerializationMedium):

#     @classmethod
#     def setUpClass(class_):
#         from loremipsum.serialization.mediums import pkg_resources_
#         class_._serializer = pkg_resources_
#         class_._args = dict(package_name=u'loremipsum')
#         class_._generator = u'loremipsum'

#     def _dump(self):
#         with self.assertRaises(NotImplementedError):
#             self._serializer.dump(self._generator, dict(), **self._args)


# class TestSerializationMediumDirectory(testing.TestSerializationMedium):

#     @classmethod
#     def setUpClass(class_):
#         from loremipsum.serialization.mediums import directory
#         class_._serializer = directory
#         class_._args = dict(prefix=PREFIX)
#         class_._generator = u'loremipsum'

#     @classmethod
#     def tearDownClass(class_):
#         directory = os.path.join(PREFIX, class_._generator)
#         for txt_file in os.listdir(directory):
#             os.remove(os.path.join(directory, txt_file))
#         os.rmdir(directory)


# class TestSerializationMediumZipFile(testing.TestSerializationMedium):

#     @classmethod
#     def setUpClass(class_):
#         from loremipsum.serialization.mediums import zipfile_
#         class_._serializer = zipfile_
#         class_._args = dict(prefix=PREFIX)
#         class_._generator = u'loremipsum'

#     @classmethod
#     def tearDownClass(class_):
#         os.remove(os.path.join(PREFIX, class_._generator + u'.zip'))


# class TestSerializationMediumFile(testing.TestSerializationMedium):

#     @classmethod
#     def setUpClass(class_):
#         from loremipsum.serialization.mediums import file_
#         class_._serializer = file_
#         class_._args = dict(prefix=PREFIX, extension=u'test')
#         class_._generator = u'loremipsum'

#     @classmethod
#     def tearDownClass(class_):
#         os.remove(os.path.join(PREFIX, class_._generator + u'.test'))
