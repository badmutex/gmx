from distutils.core import setup

setup(name='gmx',
      version='1.0.0',
      py_modules= ['gmx.classes',
                   'gmx.gmx'
                   ],

      author = "Badi' Abdul-Wahid",
      author_email = 'abdulwahidc@gmail.com',
      url = 'https://github.com/badi/gmx',
      license = 'BSD',
      description = 'Python wrappers for GROMACS executables'
      )
