def module_weights(choice):
    adf_weights = [10, 35, 20, 35]
    prg_weights = [10, 25, 30, 35]
    cnf_weights = [15, 30, 30, 25]
    icf_weights = [10, 25, 25, 15, 25]
    muf_weights = [10, 30, 25, 35]
    prc_weights = [10, 30, 30, 30]
    brp_weights = [15, 35, 20, 30]
    prt_weights = [15, 25, 20, 40]

    weights_dict = { # Map choices to weights
        "1": adf_weights,
        "2": prg_weights,
        "3": cnf_weights,
        "4": icf_weights,
        "5": muf_weights,
        "6": prc_weights,
        "7": brp_weights,
        "8": prt_weights,
    }
    return weights_dict.get(str(choice))



def enter_term_marks(weights, module_name):
    marks = []
    for i in range(len(weights)):
        while True:  # error checker so the damn thing doesn't break
            try:
                mark = float(input(f"Enter your {module_name} Term {i+1} final mark percentage (number only): "))
                if 0 <= mark <= 100:
                    marks.append(mark)
                    break
                else:
                    print("Please enter a value between 0 and 100.")
            except ValueError:
                print("Haibo!! Invalid Input.\n Please enter an actual number dude number.\n")

    # print(marks)  # testing whats in marks(remove later)
    return marks

def calculate_current_and_required(marks, weights, target_grade=50):
    # Normalize weights to percentages if they appear to be decimals (0-1 range)
    normalized_weights = []
    for weight in weights:
        if 0 <= weight <= 1:
            normalized_weights.append(weight * 100)
        elif 1 < weight <= 100:
            normalized_weights.append(weight)
        else:
            raise ValueError(f"Weight {weight} is outside valid range (0-100% or 0-1 decimal)")

    completed_terms = [(i, mark, normalized_weights[i]) for i, mark in enumerate(marks) if mark > 0]
    zero_mark_indices = [i for i, mark in enumerate(marks) if mark == 0]
    num_terms = len(marks)
    num_zero_marks = len(zero_mark_indices)

    result = {
        'current_weighted_mark': 0,
        'required_final_mark': None,
        'status': '',
        'analysis': {},
        'is_achievable': True,
        'scenario': ''
    }

    # Calculate current weighted mark from completed terms (all in 0-100 scale)
    current_weighted_sum = sum(mark * (weight / 100) for _, mark, weight in completed_terms)
    completed_weight_percentage = sum(weight for _, _, weight in completed_terms)

    result['current_weighted_mark'] = round(current_weighted_sum, 2)
    result['analysis']['completed_terms'] = len(completed_terms)
    result['analysis']['completed_weight_percentage'] = round(completed_weight_percentage, 2)

    # Scenario 1: Only the last mark is zero (calculate required final mark)
    if num_zero_marks == 1 and zero_mark_indices[0] == num_terms - 1:
        result['scenario'] = 'Calculate required final mark'
        final_term_weight = normalized_weights[-1] / 100
        required_total_points = target_grade
        current_points = current_weighted_sum
        required_final_mark = (required_total_points - current_points) / final_term_weight
        result['required_final_mark'] = round(required_final_mark, 2)
        result['analysis']['final_term_weight'] = round(normalized_weights[-1], 2)
        # Check if achievable (within 0-100 range)
        if required_final_mark < 0:
            result['status'] = f"Target already exceeded! Current mark: {current_weighted_sum:.2f}"
            result['is_achievable'] = True
        elif required_final_mark > 100:
            result['status'] = f"Target unachievable. Need {required_final_mark:.2f} but max possible is 100"
            result['is_achievable'] = False
        else:
            result['status'] = f"Need {required_final_mark:.2f}% on final term to achieve {target_grade}%"
            result['is_achievable'] = True

    # Scenario 2: Last two marks are zero OR only two terms exist with last mark zero
    elif (num_zero_marks == 2 and zero_mark_indices == [num_terms-2, num_terms-1]) or \
         (num_terms == 2 and num_zero_marks == 1 and zero_mark_indices[0] == 1):
        result['scenario'] = 'Calculate current position before final term(s)'
        if current_weighted_sum >= target_grade:
            result['status'] = f"Already above target ({target_grade}) with {current_weighted_sum:.2f}"
            result['required_final_mark'] = 0
        else:
            result['status'] = f"Below target. Current: {current_weighted_sum:.2f}, Target: {target_grade}"
            remaining_weight = sum(normalized_weights[i] / 100 for i in zero_mark_indices)
            points_needed = target_grade - current_weighted_sum
            if remaining_weight > 0:
                avg_mark_needed = points_needed / remaining_weight
                result['required_final_mark'] = round(avg_mark_needed, 2)
                if avg_mark_needed > 100:
                    result['is_achievable'] = False
                    result['status'] += f". Need average of {avg_mark_needed:.2f} across remaining terms (impossible)"
                else:
                    result['status'] += f". Need average of {avg_mark_needed:.2f} across remaining terms"
        result['analysis']['remaining_terms'] = len(zero_mark_indices)
        result['analysis']['remaining_weight'] = round(sum(normalized_weights[i] for i in zero_mark_indices), 2)

    # Scenario 3: Multiple zeros or other patterns
    else:
        result['scenario'] = 'Multiple incomplete terms'
        result['status'] = f"Current weighted mark: {current_weighted_sum:.2f} from {len(completed_terms)} completed terms"
        if len(zero_mark_indices) > 0:
            remaining_weight = sum(normalized_weights[i] / 100 for i in zero_mark_indices)
            points_needed = max(0, target_grade - current_weighted_sum)
            if remaining_weight > 0 and points_needed > 0:
                avg_mark_needed = points_needed / remaining_weight
                result['required_final_mark'] = round(avg_mark_needed, 2)
                if avg_mark_needed > 100:
                    result['is_achievable'] = False
                    result['status'] += f". Need average of {avg_mark_needed:.2f} across {len(zero_mark_indices)} remaining terms (impossible)"
                else:
                    result['status'] += f". Need average of {avg_mark_needed:.2f} across {len(zero_mark_indices)} remaining terms"
            else:
                result['status'] += ". Target already achieved or no remaining terms"
        result['analysis']['incomplete_terms'] = len(zero_mark_indices)
        result['analysis']['incomplete_term_indices'] = zero_mark_indices

    # Additional analysis
    result['analysis']['target_grade'] = target_grade
    result['analysis']['total_possible_if_perfect'] = sum(100 * (weight / 100) for weight in normalized_weights)
    return result


def welcome():
    print("\n||========================================================================================================||\n||\t\t\t\t\t\t\t\t\t\t\t\t\t  ||\n" \
    "||   Hi, welcome to your interactive grade calculator(and predictor?)\t\t\t\t\t  ||"
    "\n||   This cmd calculator will help you determine your current year mark and what you need to pass.\t  ||\n||\t\t\t\t\t\t\t\t\t\t\t\t\t  ||\n" \
    "||   You can check you mark progress for the follwoing modules:\t\t\t\t\t\t  ||\n||\t\t\t\t\t\t\t\t\t\t\t\t\t  ||\n"\
        "||  [1] ADF 152S\t\t\t\t\t\t\t\t\t\t\t  ||\n"\
        "||  [2] PRG 152S\t\t\t\t\t\t\t\t\t\t\t  ||\n"\
        "||  [3] CNF 152S\t\t\t\t\t\t\t\t\t\t\t  ||\n"\
        "||  [4] ICF 152S\t\t\t\t\t\t\t\t\t\t\t  ||\n"\
        "||  [5] MUF 152S\t\t\t\t\t\t\t\t\t\t\t  ||\n"\
        "||  [6] PRC 152S\t\t\t\t\t\t\t\t\t\t\t  ||\n"\
        "||  [7] BRP 152S\t\t\t\t\t\t\t\t\t\t\t  ||\n"\
        "||  [8] PRT 152S\t\t\t\t\t\t\t\t\t\t\t  ||\n||\t\t\t\t\t\t\t\t\t\t\t\t\t  ||\n"\
        "||========================================================================================================||\n")
    # return message

def display_results(module_name, result):
    print("\n==============================================")
    print(f"📘 Module: {module_name}")
    print("==============================================")
    print(f"Current weighted mark: {result['current_weighted_mark']}%")
    
    if result['required_final_mark'] is not None:
        print(f"Required average on remaining terms: {result['required_final_mark']}%")
    
    print(f"Status: {result['status']}")
    print("----------------------------------------------")
    print("Analysis:")
    for key, value in result['analysis'].items():
        print(f"  - {key.replace('_', ' ').capitalize()}: {value}")
    print("==============================================\n")


def module_selection():
    module_names = {
        "1": "ADF 152S",
        "2": "PRG 152S",
        "3": "CNF 152S",
        "4": "ICF 152S",
        "5": "MUF 152S",
        "6": "PRC 152S",
        "7": "BRP 152S",
        "8": "PRT 152S",
    }
    print("\nPlease select a module from the above list to check your marks.\n")

    while True:
        choice = input("Enter your choice (1-8): ")
        if choice in module_names:
            return choice, module_names[choice]  # Return both choice and name
        else:
            print("\nInvalid choice. Please enter a number between 1 and 8.")


def main():
    welcome()
    choice, module_name = module_selection()
    weights = module_weights(choice)
    marks = enter_term_marks(weights,module_name)
    # You can change the target_grade value if needed
    result = calculate_current_and_required(marks, weights, target_grade=50)
    display_results(module_name, result)

    


if __name__ == "__main__":
    main()