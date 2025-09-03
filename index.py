
from utility import create_tab

def main():
	choice=input("Press '1' for creating table.\nPress '2' for populating tables with data.")
	if choice=='1':
		create_tab()
	elif choice=='2':
		pass
	else:
		print("enter valid choice")		

if __name__ == '__main__':
		main()	