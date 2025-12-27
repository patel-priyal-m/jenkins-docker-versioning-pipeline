"""
Simple calculator application - intentionally poorly formatted for Black demo
"""

def add(a,b):
    """Add two numbers"""
    return a+b


def subtract( a, b ):
    """Subtract b from a"""
    return a-b

def multiply(a,b):
    """Multiply two numbers"""
    result=a*b
    return result

def divide(a,b):
    """Divide a by b"""
    if b==0:
        raise ValueError("Cannot divide by zero")
    return a/b


class Calculator:
    def __init__(self,name):
        self.name=name
        self.history=[]
    
    def calculate(self,operation,a,b):
        """Perform calculation and store in history"""
        if operation=="add":
            result=add(a,b)
        elif operation=="subtract":
            result=subtract(a,b)
        elif operation=="multiply":
            result=multiply(a,b)
        elif operation=="divide":
            result=divide(a,b)
        else:
            raise ValueError(f"Unknown operation: {operation}")
        
        self.history.append({"operation":operation,"a":a,"b":b,"result":result})
        return result
    
    def get_history(self):
        """Return calculation history"""
        return self.history


def main():
    """Main application entry point"""
    version_file="VERSION"
    with open(version_file,"r") as f:
        version=f.read().strip()
    
    print(f"Calculator Application v{version}")
    print("="*40)
    
    calc=Calculator("MyCalculator")
    
    # Demo calculations
    print(f"10 + 5 = {calc.calculate('add',10,5)}")
    print(f"10 - 5 = {calc.calculate('subtract',10,5)}")
    print(f"10 * 5 = {calc.calculate('multiply',10,5)}")
    print(f"10 / 5 = {calc.calculate('divide',10,5)}")
    
    print("\nCalculation History:")
    for entry in calc.get_history():
        print(f"  {entry['operation']}: {entry['a']} and {entry['b']} = {entry['result']}")


if __name__=="__main__":
    main()
