# from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file_content import write_file_content
from functions.run_python import run_python_file


def test():
    # tests for get_files_info
    # result = get_files_info("calculator", ".")
    # print("Result for current directory:")
    # print(result)
    # print("")

    # result = get_files_info("calculator", "pkg")
    # print("Result for 'pkg' directory:")
    # print(result)

    # result = get_files_info("calculator", "/bin")
    # print("Result for '/bin' directory:")
    # print(result)

    # result = get_files_info("calculator", "../")
    # print("Result for '../' directory:")
    # print(result)

    # tests for get_file_content
    # result = get_file_content("calculator", "main.py")
    # print(result)

    # result = get_file_content("calculator", "pkg/calculator.py")
    # print(result)

    # result = get_file_content("calculator", "/bin/cat")
    # print(result)

    # tests for write_file_content
    # result = write_file_content("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    # print(result)

    # result = write_file_content("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    # print(result)

    # result = write_file_content("calculator", "/tmp/temp.txt", "this should not be allowed")
    # print(result)

    # tests for run_python_file
    result = run_python_file("calculator", "main.py")
    print(result)

    result = run_python_file("calculator", "tests.py")
    print(result)

    result = run_python_file("calculator", "../main.py")
    print(result)

    result = run_python_file("calculator", "nonexistent.py")
    print(result)

    result = run_python_file("calculator", "lorem.txt")
    print(result)

    
    pass


if __name__ == "__main__":
    test()
