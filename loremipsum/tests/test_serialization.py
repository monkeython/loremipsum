"""Test serialization sub-package."""

from loremipsum import samples
from loremipsum.serialization import content_encodings
from loremipsum.serialization import content_types
from loremipsum.tests import testcases

import os
import tempfile


PREFIX = None


def setUpModule():
    globals()['PREFIX'] = tempfile.mkdtemp()


def tearDownModule():
    os.rmdir(globals()['PREFIX'])


class TestSchemeFile(testcases.TestSerializationScheme):

    @classmethod
    def setUpClass(class_):
        class_._sample = samples.DEFAULT
        class_._CannotLoadRemoved = IOError
        class_._CannotRemoveAgain = OSError
        class_._urls = {
            'file://{}/sample'.format(PREFIX): dict(),
            'file://{}/sample'.format(PREFIX): dict(
                content_type='application/json',
                content_encoding='gzip'),
            'file://{}/sample.json'.format(PREFIX): dict(),
            'file://{}/sample.json.Z'.format(PREFIX): dict()}


class TestContentTypeJson(testcases.TestSerializationContentType):

    _type = content_types.application_json


class TestContentTypeOctetStream(testcases.TestSerializationContentType):

    _type = content_types.application_octet_stream


class TestContentTypeXTar(testcases.TestSerializationContentType):

    _type = content_types.application_x_tar


class TestContentTypeZip(testcases.TestSerializationContentType):

    _type = content_types.application_zip


class TestContentEncodingCompress(testcases.TestSerializationContentEncoding):

    _encoding = content_encodings.compress


class TestContentEncodingGzip(testcases.TestSerializationContentEncoding):

    _encoding = content_encodings.gzip_


class TestContentEncodingBzip2(testcases.TestSerializationContentEncoding):

    _encoding = content_encodings.bzip2
