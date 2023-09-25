import pandas as pd
import joblib

model = joblib.load('random_forest_regressor.pkl')


def map_building_type(user_input):
    building_type_mapping = {
        'apartment': 'Apartment',
        'cottage': 'Cottage',
        'garage': 'Garage',
        'garden': 'Garden_house',
        'land': 'Land',
        'new': 'New_building',
        'object': 'Object',
        'office': 'Office',
        'old': 'Old_building',
        'plot': 'Plot',
        'secondary': 'Secondary',
    }
    return building_type_mapping.get(user_input.lower(), 'Unknown')


def encode_building_type(building_type_unified, category):
    return 1 if building_type_unified == category else 0


def get_user_selection(prompt, options):
    while True:
        print(prompt)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def predict_home_price():
    seller_type = get_user_selection("Select the seller type:", ["agent", "owner"])
    building_type_input = get_user_selection("Select the building type:",
                                             [
                                                 "apartment",
                                                 "cottage",
                                                 "garage",
                                                 "garden",
                                                 "land",
                                                 "new",
                                                 "object",
                                                 "office",
                                                 "old",
                                                 "plot",
                                                 "secondary",
                                             ]
                                             )
    is_near_metro = int(
        get_user_selection("Is the property near a metro station?", ["Yes", "No"]) == "Yes"
    )

    building_type = map_building_type(building_type_input)

    input_data = pd.DataFrame({
        'seller_type_encoded': [0 if seller_type == 'agent' else 1],
        'building_type_unified': [building_type],
        'is_near_metro': [is_near_metro]
    })

    input_data['building_type_Apartment'] = input_data['building_type_unified'].apply(
        lambda x: encode_building_type(x, 'Apartment'))
    input_data['building_type_Cottage'] = input_data['building_type_unified'].apply(
        lambda x: encode_building_type(x, 'Cottage'))
    input_data['building_type_Garage'] = input_data['building_type_unified'].apply(
        lambda x: encode_building_type(x, 'Garage'))
    input_data['building_type_Garden_house'] = input_data['building_type_unified'].apply(
        lambda x: encode_building_type(x, 'Garden_house'))
    input_data['building_type_Land'] = input_data['building_type_unified'].apply(
        lambda x: encode_building_type(x, 'Land'))
    input_data['building_type_New_building'] = input_data['building_type_unified'].apply(
        lambda x: encode_building_type(x, 'building_type_New_building'))
    input_data['building_type_Object'] = input_data['building_type_unified'].apply(
        lambda x: encode_building_type(x, 'building_type_Object'))
    input_data['building_type_Office'] = input_data['building_type_unified'].apply(
        lambda x: encode_building_type(x, 'building_type_Office'))
    input_data['building_type_Old_building'] = input_data['building_type_unified'].apply(
        lambda x: encode_building_type(x, 'building_type_Old_building'))
    input_data['building_type_Plot'] = input_data['building_type_unified'].apply(
        lambda x: encode_building_type(x, 'building_type_Plot'))
    input_data['building_type_Secondary'] = input_data['building_type_unified'].apply(
        lambda x: encode_building_type(x, 'building_type_Secondary'))
    input_data.drop('building_type_unified', axis=1, inplace=True)
    prediction = model.predict(input_data)
    print(f'Predicted home price: {round(prediction[0])}')


if __name__ == '__main__':
    predict_home_price()
