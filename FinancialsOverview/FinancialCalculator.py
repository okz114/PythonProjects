# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 16:47:35 2019

@author: Omar
"""

import glob
import pandas
import os
import matplotlib.pyplot as plt
import numpy as np


class FinancialCalculator:

    startingAmount = 12200.0
    rentBankAccount = 'DE33100100100243429121'
    sharedBankAccount = 'DE45430609678239988600'
    homeInternet = 'DE13380700590045335700'
    phoneBill = 'DE04300700100270704000'
    bensGym = 'DE06720900000001239430'
    gez = 'DE28700500000002024100'
    creditCard = '9095484104'
    contactlenses = 'DE07500210000110137891'
    amazonPrime = 7.99
    netflix = 15.99
    dazn = 11.99

    def __init__(self, folderpath):
        self.folderPath = folderpath
        self.monthlyExpDict = {}
        self.filenames = []
        self.scanfolder()


    def scanfolder(self):

        files = glob.glob(self.folderPath + '/*.csv')
        files.sort()

        for file in files:
            filename = os.path.basename(file)
            filename = os.path.splitext(filename)
            filenameOhneExt = filename[0]
            self.filenames.append(filenameOhneExt)
            self.monthlyExpDict[filenameOhneExt] = pandas.read_csv(file, delimiter=';', encoding='latin-1', decimal=',')

    def get_expenses(self):
        expenses = {}
        for filename in self.filenames:
            currTotalExp = 0
            currExp = self.monthlyExpDict[filename]
            for value in currExp.Betrag:
                if value < 0:
                    currTotalExp = currTotalExp + value
            expenses[filename] = currTotalExp
        return expenses

    def get_fixed_expenses(self):

        fixed_expenses = {}
        #fixed_expenses[rentBankAccount] = self.monthlyExpDict[]



    def get_revenue(self):
        revenue = {}
        for filename in self.filenames:
            currTotalRev = 0
            currRev = self.monthlyExpDict[filename]
            for value in currRev.Betrag:
                if value > 0:
                    currTotalRev = currTotalRev + value
            revenue[filename] = currTotalRev
        return revenue

    def show_overview(self):
        barwidth = 0.3
        expenses = self.get_expenses()
        revenue = self.get_revenue()
        expBar = [x * -1 for x in list(expenses.values())]
        revBar = list(revenue.values())

        expBase = np.arange(len(expBar))
        revBase = [x + barwidth for x in expBase]

        plt.bar(expBase, expBar, width=barwidth, color='red', label='Ausgaben')
        plt.bar(revBase, revBar, width=barwidth, color='green', label='Einkommen')
        plt.xticks([r + barwidth for r in range(len(revBar))], self.filenames)
        plt.ylabel('EUR')
        plt.legend()
        plt.grid()
        plt.savefig(self.folderPath + 'KontoÜbersicht.png')
        #plt.show()

    def show_expenses_course(self):
        barwidth = 0.3
        expenses = self.get_expenses()
        revenue = self.get_revenue()
        expBar = [x * -1 for x in list(expenses.values())]
        revBar = list(revenue.values())

        expBase = np.arange(len(expBar))
        revBase = [x + barwidth for x in expBase]
        fig = plt.figure(figsize=(18.0, 15.0))
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)
        ax1.plot(self.filenames, expBar, 'rx:', label='Ausgaben')
        ax1.plot(self.filenames, revBar, 'gx:', label='Einkommen')

        monthlySavings = [-expBar[i] + revBar[i] for i in range(len(expBar))]
        ax1.plot(self.filenames, monthlySavings, 'kx:', label='Differenz')
        ax1.legend()
        ax1.set_ylabel('EUR')
        ax1.grid()
        totalSavings = []

        for savedAmount in monthlySavings:
            if len(totalSavings) == 0:
                totalSavings.append(savedAmount + self.startingAmount)
            else:
                totalSavings.append(savedAmount + totalSavings[len(totalSavings) - 1])

        #plt.subplot(212)
        ax2.plot(self.filenames, totalSavings, 'bx:', label='Gesparrt')
        ax2.legend()
        ax2.set_ylabel('EUR')
        ax2.grid()
        plt.savefig(self.folderPath + 'KontoVerlauf.png')
        #plt.show()


if __name__ == "__main__":
    myfinancials = FinancialCalculator('D:/05_Financials/Omar_Private')
    #monthlyExp = myfinancials.scanfolder()
    myfinancials.show_overview()
    myfinancials.show_expenses_course()
