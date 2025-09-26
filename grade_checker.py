def module_weights(choice):
    adf_weights = [10, 25, 30, 35]
    prg_weights = [10, 25, 30, 35]
    cnf_weights = [15, 30, 30, 25]
    icf_weights = [10, 25, 25, 15, 25]
    muf_weights = [10, 30, 25, 35]
    prc_weights = [10, 30, 30, 30]
    brp_weights = [15, 35, 20, 30]
    prt_weights = [15, 25, 20, 45]

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


def module_selection():
    print("\nPlease select a module from the above list to check your marks.\n")

    while True:
        choice = input("Enter your choice (1-8): ")
        if choice in [str(i) for i in range(1, 9)]:
            return choice  # Return as string
        else:
            print("\n⚠️ Invalid choice. Please enter a number between 1 and 8.")


def main():
    welcome()
    choice = module_selection()
    weights = module_weights(choice)
    print(f"Selected module weights: {weights}")


if __name__ == "__main__":
    main()