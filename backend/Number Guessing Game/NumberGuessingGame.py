#----------------------------------------------------
import os
import random
import time
#----------------------------------------------------
def cleanScreen():
	if os.name == 'posix':
		_=os.system('clear')
	else:
		_=os.system('cls')
#----------------------------------------------------
def line():
    for i in range(35):
        print("-", end="-")
    print()
#----------------------------------------------------
def main():
	print("Welcome to the Number Guessing Game!")
	print("I'm thinking of a number between 1 and 100.")
	print("Which number am i thinking??")
	line()
	dificcultySelection()
#----------------------------------------------------
def dificcultySelection():
	chances=0
	print("Please select the difficulty level:")
	print("1. Easy (10 chances)")
	print("2. Medium (5 chances)")
	print("3. Hard (3 chances)")
	while True:
		try:
			line()
			selectLevel = int(input("Give your choice : "))
			if(selectLevel==1):
				input("Great!You have selected the Easy difficulty level.Press Enter to start the game!")
				chances=10
				mainGame(chances)
			elif(selectLevel==2):
				input("Great!You have selected the Medium difficulty level.Press Enter to start the game!")
				chances=5
				mainGame(chances)
			elif(selectLevel==3):
				input("Great!You have selected the Hard difficulty level.Press Enter to start the game!")
				chances=3
				mainGame(chances)
			else:
				cleanScreen()
				print("Choose 1 , 2 or 3")
				line()
				print("Please select the difficulty level:")
				print("1. Easy (10 chances)")
				print("2. Medium (5 chances)")
				print("3. Hard (3 chances)")
		except ValueError:
			cleanScreen()
			print("Invalid input. Please enter a number.")
			line()
			print("Please select the difficulty level:")
			print("1. Easy (10 chances)")
			print("2. Medium (5 chances)")
			print("3. Hard (3 chances)")
#----------------------------------------------------
def mainGame(chances):
	cleanScreen()
	random_number = random.randint(1, 100)
	attempts=0
	startTime=time.time()
	while chances>0:	
		try:
			guess=int(input("Give your guess : "))
			if (guess==random_number):
				chances-=1
				attempts+=1
				elapsedTime=time.time()-startTime
				print("Congratulations! You guessed the correct number in "+str(attempts)+" attempts.")
				print("Time taken:"+str(round(elapsedTime,2))+" seconds.")
				input("Press Enter to continue.")
				replayGame()
				break
			elif(guess<random_number):
				print("Incorrect! The number is greater than "+str(guess)+".")
				chances-=1
				attempts+=1
				if(chances!=0):
					print("You have "+str(chances)+" chances remaining!")
				else:
					print("Sorry. You lost...")
					input("Press Enter to continue.")
					replayGame()
			elif(guess>random_number):
				print("Incorrect! The number is less than "+str(guess)+".")
				chances-=1
				attempts+=1
				if(chances!=0):
					print("You have "+str(chances)+" chances remaining!")
				else:
					print("Sorry. You lost...")	
					input("Press Enter to continue.")
					replayGame()			
		except ValueError:
			print("Enter a number between 1 and 100!")
#----------------------------------------------------
def replayGame():
	cleanScreen()
	while True:
		replay=input("Would you like to play again? (Yes/No):").lower()
		if replay in ["yes", "y"]:
			cleanScreen()
			dificcultySelection()
			return
		elif replay in ["no", "n"]:
			exitCheck=input("Would you like to terminate the game? (Yes/No): ").lower()
			if exitCheck in ["yes", "y"]:
				print("Thanks for playing! Goodbye.")
				exit()
			else:
				replayGame()
				return
		else:
			print("Invalid input. Please enter 'Yes' or 'No'.")			
#--------------------MAIN----------------------------
if __name__ == "__main__":
    main()
