<<<<<<< HEAD
from user_input import user_input
from utils import preprocess_and_predict, utils
from Email_Notifier import mail_sender

def main():

    print('collecting user input')
    test_df = user_input()

    print('Loading the models')
    std_scaler, iso_cls, rf_cls = utils()

    print('Performing the Prediction')
    prediction, result = preprocess_and_predict(test_df, std_scaler, iso_cls, rf_cls)

    if prediction == 1:
        print('sending Mail if Fraudulent Transaction occur')
        mail_sender(result)

    return prediction, result


if __name__ == "__main__":
    main()

=======
>>>>>>> 66fb15086bb33ddbf384c19b96ec8013bf8b720b
