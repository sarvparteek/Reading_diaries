class Reader:
    def __init__(self, series, daily_target=10):
        self.data = series  # pandas series
        self.name = series.name
        self.week_length = 7
        self.week = dict() # keys: violations, eff_violations
        #self.week2 = dict() # keys: violations, eff_violations
        self.mean_pages = 0
        self.total_pages = 0
        self.fine_per_violation = 5
        self.fines = 0
        self.violations = 0
        self.eff_violations = 0
        self.daily_target = daily_target
        
    def computeWeekViolations(self, data, results):
        results["violations"] = 0

        # There is a violation if the daily target is not achieved on two consecutive days
        for i in range(self.week_length - 1):
            if data.iloc[i] < self.daily_target and data.iloc[i+1] < self.daily_target:
                results["violations"] += 1

        # If pages worth daily_target times number of days in the week are read by the end of the week, then the
        # effective number of violations are zero.
        if data.sum() >= self.week_length * self.daily_target:
            results["eff_violations"] = 0
        else:
            results["eff_violations"] = results["violations"]

    def process(self):
        self.computeWeekViolations(self.data.head(self.week_length), self.week)
        #self.computeWeekViolations(self.data.tail(self.week_length), self.week2)
        self.total_pages = self.data.sum()
        self.mean_pages = self.total_pages / self.week_length
        self.violations = self.week["violations"] #+ self.week2["violations"]
        self.eff_violations = self.week["eff_violations"] #+ self.week2["eff_violations"]
        # Weekly violation counting system skips the case where someone didn't read on the last day of week 1 and first
        # day of week 2
        #if self.data.iloc[self.week_length - 1] < self.daily_target: #and \
           #self.data.iloc[self.week_length] < self.daily_target:
        #    self.violations += 1
        #    self.eff_violations += 1

        self.fines = self.fine_per_violation * self.eff_violations
