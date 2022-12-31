# define a function sigma(x_i, x_j) such that e^(1 * (x_i == x_j))
using Printf

n = 10 # initialise the number of states in the application.

number_of_states_combinations = 2 ^ n # calculate the number of states combinations.

println("The number of states combinations is: ", number_of_states_combinations)

# initialise the input states as an array size (number_of_states_combinations, n)
input_states = zeros((number_of_states_combinations, n))

binary_values = [0, 1] # define the binary variables

global index_val = 1

for v_1 in binary_values

    for v_2 in binary_values

        for v_3 in binary_values

            for v_4 in binary_values

                for v_5 in binary_values

                    for v_6 in binary_values

                        for v_7 in binary_values

                            for v_8 in binary_values

                                for v_9 in binary_values

                                    for v_10 in binary_values

                                        global input_states[index_val, :] = [v_1, v_2, v_3, v_4, v_5, v_6, v_7, v_8, v_9, v_10]

                                        global index_val = index_val + 1

                                    end
                                
                                end
                            
                            end

                        end
                    
                    end
                
                end

            end
        
        end
    
    end

end

betas = [0.01 1 4] # define a vector of beta values

# iterate through the beta values
for beta in betas 
    global f_1 = zeros((number_of_states_combinations, 1))

    for i = 1 : number_of_states_combinations # iterate through the rows.

        global identical = 0

        for j = 1 : 9 # iterate through each column states.

            if input_states[i, j]  == input_states[i, j + 1]
                global identical = identical + 1
            end
        
        end

        # e ^ beta * identical
        f_1[i] = exp(beta * identical)

    end

    # displays the f_1 values
    # println("The f_1 values for beta = ", beta, " are: ", f_1)

    global f_2 = zeros((number_of_states_combinations, 1))

    # double loop for the different states
    for i = 1 : number_of_states_combinations

        for j = 1 : number_of_states_combinations

            global identities = 0

            for k = 1 : 9

                if input_states[i, k] == input_states[j, k] 

                    global identities = identities + 1 # computes the number of identities

                end

            end

            f_2[i] = f_1[j] * exp(beta * identities) # computes the f_2 values

        end
    
    end

    # f_3 is a product between f_1 and f_2
    f_3 = f_1 .* f_2

    # applies normalisation for f_3
    f_3 = f_3 / sum(f_3)

    # initialise the previous message variable as f_3
    global previous_message =  f_3

    for i = 3 : 11

        message = zeros((number_of_states_combinations, 1))

        for j = 1 : number_of_states_combinations

            for k = 1 : number_of_states_combinations

                global identities = 0

                for l = 1 : 9

                    if input_states[j, l] == input_states[k, l]

                        global identities = identities + 1

                    end

                end

                message[j] += previous_message[k] * exp(beta * identities)

            end

        end

        global previous_message =  f_1 .* message

        global previous_message =  previous_message / sum(previous_message) # normalisation

    end

    # the indices are where the final value is equal to first value
    indicies = input_states[:, 1] .== input_states[:, 10]

    # initialise probability as 0
    global probability = 0

    for i = 1 : number_of_states_combinations

        if indicies[i] == true

            global probability += previous_message[i]

        end

    end

    # displays the probability
    println("The probability for beta = ", beta, " is: ", probability)

end



print("Successfully executed the code.")