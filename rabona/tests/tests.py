import unittest


if __name__ == '__main__':
    suites = unittest.TestLoader().discover('./tests/', pattern='test_*.py')
    runner = unittest.TextTestRunner()
    runner.run(suites)
