import subprocess
import sys

def review_files():
    # Run cleaner.py using the same Python interpreter as the current script
    subprocess.run([sys.executable, '__tools__/cleaner.py'])

def main():
    while True:
        response = input("You are about to empty the session file. Would you like to review your data? (yes/no/exit): ").strip().lower()

        if response == 'yes':
            review_files()
            print("Review completed.")

        elif response == 'no':
            print("Skipping review.")

        elif response == 'exit':
            print("Exiting program.")
            break  # Exit the loop, thus ending the program

        else:
            print("Invalid input. Please enter 'yes', 'no', or 'exit'.")

if __name__ == '__main__':
    main()
