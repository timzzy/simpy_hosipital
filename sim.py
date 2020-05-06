import simpy
import random


RANDOM_SEED = 40
PATIENT_ARRIVAL = 15        # create a new patient every 15 minutes of simulation time
NO_OF_BED = 14              # Number of beds in the Hospital (assume the summation of the hospital bed)
TIME_OF_SIMULATION = 30     # time of simulation in weeks
ADMISSION_DURATION = 5      # duration of which a patient is admitted in the hospital in weeks
CREATE_CORONA_PATIENT = 5   # create the initial corona patients


#//Lets create an hospital class
class Hospital(object):
    
    """
     A hospital has some number of beds(which they may be limited in number, depending on rate of infection),
     when new infected patients are brought to the hospital, they are placed in one of the available free beds in the ward
    """
    
    def __init__(self, env, no_of_bed, admission_duration):
        self.env = env
        self.bed = simpy.Resource(env, no_of_bed)
        self.admission_duration = admission_duration

    def admit(self, patient):
        """
            The admission  stage for a patient
        """
        yield self.env.timeout(ADMISSION_DURATION)
        #print("Patient recovery rate %d%% of %s's patient's infection." %(random.randint(50, 99), patient))
        print(patient, "'s recovery rate: ", random.randint(50, 99),"%" )
        
        
        
def patient(env, name, hosp):
    """
        The patient arrives at the hospital and is allocated a bed for treatment: patient is attended to
        name is the 'name' of a particular patient
    """
    
    print('%s arrives at the hospital at %.2f.' % (name, env.now))
    with hosp.bed.request() as request:          #every patient request  new admission bed
        yield request

        print('%s is admitted to ICU at %.2f.' % (name, env.now))
        yield env.process(hosp.admit(name))

        
        print('%s recover and leaves the hospital at %.2f.' % (name, env.now))
        
        


####the implementation setup method 
def setup(env, no_of_bed, admission_duration, patient_arrival):
    """A hospital  is created, soem randomized number of patients are created, and new patients are created every  ``patient_arrival`` minutes.
    """
    # Create the hospital
    hospital = Hospital(env, no_of_bed, admission_duration)

    # initialize some patients
    
    for i in range(CREATE_CORONA_PATIENT):
        env.process(patient(env, 'Patient %d' % i, hospital))

    # while the simulation is running, we create more randon patient to be addmitted to the hospital
    while True:
        yield env.timeout(random.randint(admission_duration - 4, admission_duration + 4))
        i += 1
        env.process(patient(env, 'Patient %d' % i, hospital))    #new created patient
       
        
        
# The simulation is setup and starteds
print('Hospital Ward \n')
random.seed(RANDOM_SEED)  # This helps reproducing the results

# A sample environment is created, then the setup process is initiated
env = simpy.Environment()
env.process(setup(env, NO_OF_BED, ADMISSION_DURATION, PATIENT_ARRIVAL))

# Execution of the program
env.run(until=TIME_OF_SIMULATION)
