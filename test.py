import unittest
import re

def validaCep(cep):

    step1 = False

    if re.match(r'^([1-9][\d]{5})$',cep):
        step1 = True
        
    if (cep[0] != cep[2] 
    and cep[1] != cep[3] 
    and cep[2] != cep[4] 
    and cep[3] != cep[5]) & step1==True:
        return True
    else:
        return False

class TesteValidaCep(unittest.TestCase):

    def testeValidaCep(self):

        self.assertEqual(validaCep('123456'),True)
        self.assertEqual(validaCep('921992'),True)
        self.assertEqual(validaCep('023456'),False)
        self.assertEqual(validaCep('123456231'),False)
        self.assertEqual(validaCep('999999'),False)
        self.assertEqual(validaCep(' 24129'),False)
        self.assertEqual(validaCep('9a2910'),False)
        self.assertEqual(validaCep('249409'),False)
        self.assertEqual(validaCep('544-32'),False)

if __name__ == "__main__":
    unittest.main()