#Importing the necessary libraries

import random
import matplotlib.pyplot as plt
import pandas as pd

#to read number of days
n=0
#Simulation of disease outbreaks
class Simulation():
    
    def __init__(self):
        #class attributes
        self.day_number = 1
        #Getting user input
        print("Disease Outbreak Simulation")
        print("\nBased on statistical assumptions.")
        print("1. We must know the total population size")
        self.population_size = int(input("Enter the population size: "))
        
        print("\n2. First theoretical assumption is that a part of the population is infected.")
        self.infection_percent = float(input("Enter the percentage (0-100) of the population who are already infected: "))
        self.infection_percent /= 100
        
        print("\n3. We must know the risk a person has to contract the disease when he is exposed to the pathogens.")
        self.infection_probability = float(input("Enter the probability (0-100) that an individual gets infected when exposed to the pathogens: "))
        
        print("\n4. We must know how many days infection will last when exposed")
        self.infection_duration = int(input("Enter the average duration (in days) the infection lasts in a person: "))
        
        print("\n5. Next required data is the mortality rate of those who are exposed")
        self.mortality_rate = float(input("Enter the mortality rate (0-100) of the infection: "))
        
        print("\n6. We need information on how many days simulation is to be run")
        print("\n   Please keep input under 100 Days.")
        n= int(input("Enter the number of days to simulate: "))
        self.sim_days=n
        

#Taking empty lists to store data        
df_day_list=[]
df_infected_list= []
df_death_list=[]
df_death_percent=[]
df_infect_percent=[]
        
class Person():
    #Class modelling any particular individual
    def __init__(self):
        #Now initialize the class attributes
        self.is_infected = False #By default, person starts healthy, not infected
        self.is_dead = False #By default, person starts ALIVE
        self.days_infected = 0 #Keeps track of days infected for individual person
        
    def infect(self, simulation):
        #To infect a person based on simulation constraints
        #random number generated to be kept less than infection_probability
        #as higher must not be allowed for successful simulation
        if random.randint(0, 100) < simulation.infection_probability:
            #if the randomly generated value is less than the infection probability
            #person is considered infected
            self.is_infected= True
            
        
    def heal(self):
        #Healing a person from infection
        self.is_infected = False
        self.days_infected = 0
        
    def die(self):
        #For the death of an individual
        self.is_dead = True
        
    def update(self, simulation):
        #Update of an individual person if they are not dead
        #Check if they are infected
        #If infected, increase the days infected count
        #Simulate if to die or to be healed
        
        #First check if person is dead or not
        if not self.is_dead:
            #Check if person is infected
            if self.is_infected:
                self.days_infected += 1
                #Simulation of whether the person will die
                #Here also, a random probability of dying is taken
                #If the value is less than the simulation mortality rate, person is considered dead
                if random.randint(0, 100) < simulation.mortality_rate:
                    self.die()
                #Check if infection is over
                #If over heal the person
                #Checking is done on the basis of on average how many days infection persists in a person
                #If the day count of total usual infection period is reached, person is considered healed
                elif self.days_infected == simulation.infection_duration:
                    self.heal()
                    
class Population():
    #Class to model the whole population
    def __init__(self, simulation):
        
        #Now initialize the attributes
        self.population = [] #list to hold all Person instances that are created
        
        #Here, all the person would be an instance of the class 
        #Creating the correct number of Person instances
        for i in range(simulation.population_size):
            person = Person()
            #Adding the person to the population
            self.population.append(person)
            
    def initial_infection(self, simulation):
        
        #As mentioned, we have to assume an initial percent of the population to be infected
        #Initial number of infection is found by taking the pop size *infection percentage
        #The value has to be round to 0 decimals and cast to an int
        #This is done taking in mind that we have to run a loop
        #Also there cannot be fractional persons, or can there be? :-)
        infected_count = int(round(simulation.infection_percent*simulation.population_size, 0))
        
        #Infect the appropriate number of people according to the conditions
        for i in range(infected_count):
            #Infect the "i"th person in the population attribute
            #Implementing that they are infected
            self.population[i].is_infected = True
            #Initiating their day of infection to be one
            self.population[i].days_infected = 1
            
        #Now we need to suffle the values so the infection spread is uniform
        random.shuffle(self.population)

    def spread_infection(self, simulation):
        #Spreading the infection to the adjacent people in the population list
        #This is done so as to keep in mind that people get infected from people near them
        
        #Iterating via a for loop through the entire population
        for i in range(len(self.population)):
            #The "i"th person is ALIVE, simulate if they can get infected
            #already dead people will not be infected
            #Check to see if adjacent people are infected
            
            #Checking if the person is not dead
            if self.population[i].is_dead == False:
                #We start with the first person in the list, can only check to the right
                if i == 0:
                    if self.population[i+1].is_infected:
                        #If adjacent person is infected, we initiate simulation of infection in "i" person
                        self.population[i].infect(simulation)
                        
                #"i" is in the middle of the list
                #Now can check to the left [i-1] and right [i+1]
                elif i < len(self.population)-1:
                    if self.population[i-1].is_infected or self.population[i+1].is_infected:
                        #If either of the adjacent person is infected,we initiate simulation of infection in "i" person
                        self.population[i].infect(simulation)
                        
                #Now "i" is the last person in the list
                #We can only check to the left [i-1]
                
                elif i == len(self.population)-1:
                    if self.population[i-1].is_infected:
                        #If adjacent person is infected, we initiate simulation of infection in "i"
                        self.population[i].infect(simulation)
                        
    
    def update(self, simulation):
        #Update the whole population by updating each individual person
        #Increase simulation day by 1
        simulation.day_number += 1
        
        #Calling the update method for all person instances in the population
        for person in self.population:
            person.update(simulation)
            
            
    def display_statistics(self, simulation):
        #Current statistics
        #Initialize values
        total_infected_count = 0
        total_death_count = 0
        
        #Looping through whole population
        for person in self.population:
            #Infected person
            if person.is_infected:
                total_infected_count += 1
                #Dead person
                if person.is_dead:
                    total_death_count += 1
                    
        #Percentage of population that is infected and dead
        infected_percent = round(100*(total_infected_count/simulation.population_size), 4)
        death_percent = round(100*(total_death_count/simulation.population_size), 4)
        
        df_infected_list.append(total_infected_count)
        df_death_list.append(total_death_count)
        df_day_list.append(simulation.day_number)
        df_death_percent.append(death_percent)
        df_infect_percent.append(infected_percent)
        
        
        
        
   
#The main code
        
sim = Simulation()
pop = Population(sim)

#Set the initial infection conditions of the population
pop.initial_infection(sim)
pop.display_statistics(sim)

input("\nPress enter to start the simulation")

#Run the simulation

for i in range(1, sim.sim_days):
    #Single day, spread the infection, update the population, display statistics
    pop.spread_infection(sim)
    pop.update(sim)
    pop.display_statistics(sim)
    
    
        
        
        
        
#print(df_day_list)

#print(df_infected_list)

#print(df_death_list)           
            
data = {'Day': df_day_list, 'Infected': df_infected_list, 'Deaths': df_death_list, 'Infected Percent': df_infect_percent, 'Death Percent': df_death_percent } 
df = pd.DataFrame(data) 

file_name = 'Disease.xlsx'
  
# saving the excel
df.to_excel(file_name)

print("All data in the Excel file!")
 
print("\nThe simulation infected cases and deaths over the days:")
         
plt.plot(df_day_list, df_infected_list, label = "Infected")  
plt.plot(df_day_list, df_death_list, label = "Deaths")
plt.xlabel('Day')
plt.ylabel("Number of people")
plt.title('CASES')  
plt.legend()
plt.show()
        
                    
                    
                    
                    
                
                
        

                        
                        
        
        
                
        

        

