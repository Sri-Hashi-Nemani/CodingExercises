import os
import requests
import pandas as pd
import time


class CurrencyExchange:

    # Internal Method
    def _get_currency_dict(self):
        """
        Get the response from currencies endpoint and create a dictionart with currency_code
        and currencty details. This is to retrive the data in efficient way
        """
        try:
            currency_details = requests.get('https://api.coinbase.com/v2/currencies').json()['data']
        except:
            raise Exception("Unable to fetch the Currency details")
        currency_dict = {}
        for data in self.__currency_details:
            currency[data['id']] = data['name']
        return currency_dict      
            
    def get_currency_name(self, currency_code):
        """
        Fetch the currency name for the given currency code
        :param: currency code fow which currency has to be retrieved
        :return: currency name
        """
        return self._get_currency_dict[currency_code.upper()]
    
    def get_currency_exchange_rates(self, currency_code):
        """
        Fetch the currency exchange rates for a given currenct code and write the details
        into the csv file
        """
        try:
            response = requests.get("https://api.coinbase.com/v2/exchange-rates",
                                     params={'currency': currency_code.upper()}).json()['data']
        except:
            raise Exception("Unable to fetch the exchange rate for the given currency code")
            
        # Fetching the currency name for all the exchange rates using the currency code mentiones in
        # rates dictionary
        currency = []
        for rates in response['rates']:
            currency.append(self.get_currency_name(rates))
            
        # Creating dataframe with 2 columns
        exchange_result = pd.DataFrame(response['rates'].items(), columns=['currency_code', 'exchange_rate'])
        # Updating the base currenvcy values are same for all the rows as it is same for all the rows
        exchange_result['base_currency_code'] = currency_code
        exchange_result['base_currency'] = self.get_currency_name(currency_code)
        exchange_result['currency'] = currency
        
        # Creating the output folder if not available
        if not os.path.isdir('Output'):
            os.mkdir('Output')     
            
        # Creating the output file
        exchange_result.to_csv('Output/{}-exchange_output.{}.csv'.format(currency_code, time.time(), index=False,
                      columns=['base_currency_code', 'base_currency', 'currency_code', 'currency', 'exchange_rate'])
                               
    def get_btc(self, currency_code, option):
        """
        Fetch the bitcoin currency values for buyt/sell/spot for a given currency code
        """
        options = {'a': 'buy', 'b': 'sell', 'c': 'spot'}
        return requests.get("https://api.coinbase.com/v2/prices/BTC-{}/\
        {}".format(currency_code, options[option]).json()['data']['amount']
        response.json()['data']['amount'])
    
 if __name__ == "__main__":
    obj = CurrencyExchange()
    while True:
        print("Please see the below menu and select the options(a/b/c/d) accordingly\n\
        a. Get the currency name for the given currency code\n\
        b. Currency exchange Rates\n\
        c. Bitcoin Buy/sell/Spot prices\n\
        d. Quit")
        data = input()        
        if data == 'a':
            currency_code = input("Enter the currency Code:")
            print(obj.get_currency_name(currency_code))
        elif data == 'b':
            currency_code = input("Enter the currency Code:")
            print(obj.get_currency_exchange_rates(currency_code))            
        elif data == 'c':
            currency_code = input("Enter the currency Code:")                   
            print("Please select the option(a/b/c) from the below menu\n\
            a. Buy\n\
            b. Sell\n\
            c. Spot Price\n")
            option = input()
            if option not in ['a', 'b', 'c']:
                print("Exiting the application as the input does not match with the given options")
                break
            print(obj.get_btc(currency_code, option))    
        else:
            print("Exiting the application as the input does not match with the given options")
            break
