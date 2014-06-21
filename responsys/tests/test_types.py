import unittest

from mock import Mock

from ..types import (
    InteractType, InteractObject, ListMergeRule, RecordData, Record, DeleteResult, LoginResult,
    MergeResult, RecipientResult, ServerAuthResult)


class InteractTypeTests(unittest.TestCase):
    """ InteractType instance """
    def setUp(self):
        self.type = InteractType(foo='bar')
        self.client = Mock()

    def test_soap_attribute_method_sets_attribute(self):
        """soap_attribute method sets attribute """
        self.type.soap_attribute('red', True)
        self.assertTrue(self.type.red)

    def test_soap_attribute_method_registers_attribute(self):
        """soap_attribute method registers attribute """
        self.type.soap_attribute('blue', True)
        self.assertIn('blue', self.type._attributes)

    def test_soap_name_property_returns_class_name(self):
        """soap_name property returns class name """
        self.assertEqual(self.type.soap_name, self.type.__class__.__name__)

    def test_instance_provides_attributes_through_dictionary_lookup(self):
        self.assertEqual(self.type.foo, self.type['foo'])

    def test_get_soap_object_method_returns_client_factory_type(self):
        """get_soap_object_method returns client factory type """
        soap_object = self.client.factory.create.return_value = Mock()
        self.assertEqual(self.type.get_soap_object(self.client), soap_object)

    def test_get_soap_object_method_returns_object_with_correct_attributes_set(self):
        """get_soap_object method returns object with correct attributes set """
        self.type.soap_attribute('red_fish', True)
        soap_object = self.type.get_soap_object(self.client)
        self.assertTrue(all(
            [hasattr(soap_object, attr) for attr in ['redFish', 'foo']]))


class InteractTypeChildTests(unittest.TestCase):
    """ InteractType descendant """
    @classmethod
    def generate_type_methods(cls, types_and_expectations):
        """ Auto generates test methods for type attribute tests """
        for TypeClass, init, attrs in types_and_expectations:
            def create_test_func(TypeClass, init, attrs):
                def test_method(self):
                    instance = TypeClass(**init)
                    for attr in attrs:
                        self.assertEqual(getattr(instance, attr), attrs[attr])

                test_method.__name__ = 'test_%s_has_expected_attributes' % TypeClass.__name__
                return test_method

            test_method = create_test_func(TypeClass, init, attrs)
            setattr(cls, test_method.__name__, test_method)

        return

InteractTypeChildTests.generate_type_methods([
    # (TypeToTest
    #   init_kwargs,
    #   attrs_expectations)
    (InteractObject,
        {'folder_name': 'blarg', 'object_name': 'fuuuuu'},
        {'folder_name': 'blarg', 'object_name': 'fuuuuu'}),
    (DeleteResult,
        {'delete_result': Mock(errorMessage='', success=True, exceptionCode='', id=1)},
        {'error_message': '', 'success': True, 'exception_code': '', 'id': 1}),
    (LoginResult,
        {'login_result': Mock(sessionId=1)},
        {'session_id': 1}),
    (ListMergeRule,
        {'insert_on_no_match': 'A'},
        {'insert_on_no_match': 'A'}),
    (MergeResult,
        {'merge_result': Mock(insertCount=1, updateCount=1, rejectedCount=1, totalCount=3,
         errorMessage='Blarg')},
        {'insert_count': 1, 'update_count': 1, 'rejected_count': 1, 'total_count': 3,
         'error_message': 'Blarg'}),
    (RecipientResult,
        {'recipient_result': Mock(recipientId=1, errorMessage='Blarg')},
        {'recipient_id': 1, 'error_message': 'Blarg'}),
    (ServerAuthResult,
        {'server_auth_result': Mock(authSessionId=1, encryptedClientChallenge='boo',
         serverChallenge='ahhh')},
        {'auth_session_id': 1, 'encrypted_client_challenge': 'boo', 'server_challenge': 'ahhh'})
])
