from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter import ttk
import json


class CalculatorApp:

    def __init__(self):
        self.authorization_data = {}
        self.authoriz_window = Tk()
        self.authoriz_window.title("Calories Calculator")
        self.authoriz_window.geometry("350x520")
        self.setup_authorization_window()

    def setup_authorization_window(self):

        name_label = Label(self.authoriz_window, text="Your name:")
        name_label.grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = Entry(self.authoriz_window)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        password_label = Label(self.authoriz_window, text="Password:")
        password_label.grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = Entry(self.authoriz_window, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.gender = StringVar()
        self.gender.set(' ')
        gender_male = Radiobutton(self.authoriz_window, text="Male", variable=self.gender, value="Male")
        gender_female = Radiobutton(self.authoriz_window, text="Female", variable=self.gender, value="Female")
        gender_male.grid(row=2, column=0, padx=10, pady=5)
        gender_female.grid(row=2, column=1, padx=10, pady=5)

        weight_label = Label(self.authoriz_window, text="Weight (kg):")
        weight_label.grid(row=3, column=0, padx=10, pady=5)
        self.weight_combobox = Combobox(self.authoriz_window, values=[str(i) for i in range(20, 151)], state="readonly")
        self.weight_combobox.grid(row=3, column=1, padx=10, pady=5)

        height_label = Label(self.authoriz_window, text="Height (cm):")
        height_label.grid(row=4, column=0, padx=10, pady=5)
        self.height_combobox = Combobox(self.authoriz_window, values=[str(i) for i in range(100, 251)], state="readonly")
        self.height_combobox.grid(row=4, column=1, padx=10, pady=5)

        age_label = Label(self.authoriz_window, text="Select Age:")
        age_label.grid(row=5, column=0, padx=10, pady=5)
        self.age_combobox = Combobox(self.authoriz_window, values=[str(i) for i in range(4, 121)], state="readonly")
        self.age_combobox.grid(row=5, column=1, padx=10, pady=5)

        activity_label = Label(self.authoriz_window, text="Select Activity Level:")
        activity_label.grid(row=6, column=0, padx=10, pady=5)

        activity_levels = [
            ("Moderate", 1.375),
            ("Medium", 1.55),
            ("High Active", 1.725),
            ("Extremely High Active", 1.9)
        ]

        activity_info = {
            None: None,
            1.375: "Light sports 1-3 days/week, sedentary work, housekeeper work",
            1.55: "Sedentary work + exercise 3-5 days/week, easy work on feet up to 12 hours",
            1.725: "Intense exercise, sports 6-7 times a week, work on the legs with intense sports",
            1.9: "Athletes and people doing similar activities 6-7 times a week"
        }

        def update_activity_info():
            selected_activity = float(self.activity_coef.get())
            activity_info_label.config(text=activity_info[selected_activity], background="white")

        activity_info_label = Label(self.authoriz_window, text=activity_info[None], wraplength=300, justify=CENTER)
        activity_info_label.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

        self.activity_coef = StringVar()
        self.activity_coef.set(' ')
        for i, (text, value) in enumerate(activity_levels):
            activity_radio = Radiobutton(self.authoriz_window, text=text, variable=self.activity_coef, value=value,
                                         command=update_activity_info)
            activity_radio.grid(row=6 + i, column=1, padx=10, pady=5)

        goal_label = Label(self.authoriz_window, text="Select your goal:")
        goal_label.grid(row=11, column=0, padx=10, pady=5)

        self.goal = StringVar()
        self.goal.set(' ')
        weight_goals = [("Lose", "lose"), ("Maintain", "maintain"), ("Gain", "gain")]

        for i, (text, value) in enumerate(weight_goals):
            goal_radio = Radiobutton(self.authoriz_window, text=text, variable=self.goal, value=value)
            goal_radio.grid(row=11 + i, column=1, padx=10, pady=5)

        save_button = Button(text="Save", command=self.save_click, width=10)
        save_button.grid(row=15, column=1, padx=10, pady=5)

    def validate_data(self):

        name = self.name_entry.get()
        password = self.password_entry.get()

        if len(name) < 3 or len(password) < 8:
            messagebox.showerror("Error", "Please, enter name with >=3 letters and password with >=8 symbols")
            return False

        selected_gender = self.gender.get()
        if selected_gender == ' ':
            messagebox.showerror("Error", "Please select your gender.")
            return False

        weight_str = self.weight_combobox.get()
        height_str = self.height_combobox.get()
        age_str = self.age_combobox.get()
        if not (weight_str and height_str and age_str):
            messagebox.showerror("Error", "Please select all weight, height, and age")
            return False

        selected_activity = self.activity_coef.get()
        if selected_activity == ' ':
            messagebox.showerror("Error", "Please select your activity level.")
            return False

        selected_goal = self.goal.get()
        if selected_goal == ' ':
            messagebox.showerror("Error", "Please, select your goal.")
            return False

        return True

    def save_data(self):
        self.authorization_data["name"] = self.name_entry.get()
        self.authorization_data["password"] = self.password_entry.get()
        self.authorization_data["gender"] = self.gender.get()
        self.authorization_data["weight"] = int(self.weight_combobox.get())
        self.authorization_data["height"] = int(self.height_combobox.get())
        self.authorization_data["age"] = int(self.age_combobox.get())
        self.authorization_data["activity_coefficient"] = float(self.activity_coef.get())
        self.authorization_data["goal"] = self.goal.get()

    def save_click(self):
        if self.validate_data():
            self.save_data()
            self.create_calculator_page()
            self.setup_calculator_page(self.main_calculator)
            self.authoriz_window.destroy()

    def create_calculator_page(self):
        self.main_calculator = Tk()
        self.main_calculator.title("Calories Calculator")
        self.setup_calculator_page(self.main_calculator)

    def setup_calculator_page(self, main_calculator):

        user_bmi = self.bodymass_index(self.authorization_data["weight"], self.authorization_data["height"])
        user_bmr = self.basalmet_rate(
            self.authorization_data["height"],
            self.authorization_data["weight"],
            self.authorization_data["gender"],
            self.authorization_data["age"]
        )

        average_calories_norm = self.calories_norm(user_bmr, self.authorization_data["activity_coefficient"])

        self.user_calories_norm, self.user_proteins, self.user_fats, self.user_carbs = self.calculate_user_nutrition(
            average_calories_norm,
            self.authorization_data["goal"]
        )

        welcome_label = Label(
            self.main_calculator,
            text=f"Welcome to Calories Calculator App, {self.authorization_data['name']}!",
            font=("Times New Roman", 14, "bold"), fg="green", background="white"
        )
        welcome_label.grid(row=0, column=0, padx=10, pady=5)

        if user_bmi < 18.5:
            bmi_label = Label(main_calculator, text=f"Your BMI is {user_bmi}.\n "
                                                    f"Your mass is underweight!", background="white")
            bmi_label.grid(row=1, column=0, padx=10, pady=5)
        elif 18.5 <= user_bmi < 25:
            bmi_label = Label(main_calculator, text=f"Your BMI is {user_bmi}.\n"
                                                    f"Your mass is healthy!", background="white")
            bmi_label.grid(row=1, column=0, padx=10, pady=5)
        elif 30 <= user_bmi < 35:
            bmi_label = Label(main_calculator, text=f"Your BMI is {user_bmi}.\n"
                                                    f"You have obese clas I!", background="white")
            bmi_label.grid(row=1, column=0, padx=10, pady=5)
        elif 35 <= user_bmi < 40:
            bmi_label = Label(main_calculator, text=f"Your BMI is {user_bmi}.\n"
                                                    f"You have obese clas II!", background="white")
            bmi_label.grid(row=1, column=0, padx=10, pady=5)
        else:
            bmi_label = Label(main_calculator, text=f"Your BMI is {user_bmi}.\n"
                                                    f"You have obese clas III!", background="white")
            bmi_label.grid(row=1, column=0, padx=10, pady=5)

        calories_norm_label = Label(
            main_calculator,
            text=f"Your daily calories norm based on your goal is {round(self.user_calories_norm)} cal", background="white"
        )
        calories_norm_label.grid(row=2, column=0, padx=10, pady=5)

        user_calories_norm, user_proteins, user_fats, user_carbs = self.calculate_user_nutrition(
            average_calories_norm,
            self.authorization_data["goal"]
        )

        self.authorization_data["user_calories_norm"] = user_calories_norm
        self.authorization_data["user_proteins"] = user_proteins
        self.authorization_data["user_fats"] = user_fats
        self.authorization_data["user_carbs"] = user_carbs

        pfc_label = Label(
            main_calculator,
            text=f"Your goal is to {self.goal} weight. Your daily intake of nutrients should be:\n"
                 f"{self.user_proteins} gram of proteins\n"
                 f"{self.user_carbs} gram of carbohydrates\n"
                 f"{self.user_fats} gram of fats", background="white"
        )
        pfc_label.grid(row=3, column=0, padx=10, pady=5)

        table_button = Button(main_calculator, text="Open table", command=self.open_table)
        table_button.grid(row=4, column=0, padx=10, pady=5)

        consumed_frame = Frame(main_calculator, bg="white")
        consumed_frame.grid(row=5, column=0, padx=10, pady=10)

        consumed_calories_label = Label(consumed_frame, text="Consumed Calories:")
        consumed_calories_label.grid(row=0, column=0, padx=5, pady=5)
        self.consumed_calories_entry = Entry(consumed_frame)
        self.consumed_calories_entry.grid(row=0, column=1, padx=5, pady=5)

        consumed_proteins_label = Label(consumed_frame, text="Consumed Proteins (g):")
        consumed_proteins_label.grid(row=1, column=0, padx=5, pady=5)
        self.consumed_proteins_entry = Entry(consumed_frame)
        self.consumed_proteins_entry.grid(row=1, column=1, padx=5, pady=5)

        consumed_fats_label = Label(consumed_frame, text="Consumed Fats (g):")
        consumed_fats_label.grid(row=2, column=0, padx=5, pady=5)
        self.consumed_fats_entry = Entry(consumed_frame)
        self.consumed_fats_entry.grid(row=2, column=1, padx=5, pady=5)

        consumed_carbs_label = Label(consumed_frame, text="Consumed Carbohydrates (g):")
        consumed_carbs_label.grid(row=3, column=0, padx=5, pady=5)
        self.consumed_carbs_entry = Entry(consumed_frame)
        self.consumed_carbs_entry.grid(row=3, column=1, padx=5, pady=5)

        calculate_consume_button = Button(consumed_frame, text="Calculate Deficit/Surplus",
                                          command=self.calculate_deficit_surplus)
        calculate_consume_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.deficit_surplus_label = Label(consumed_frame, text="")
        self.deficit_surplus_label.grid(row=5, column=0, columnspan=2, pady=5)

        note_label = Label(consumed_frame, text=f"Note: minus '-' means deficit", background="white", fg="green")
        note_label.grid(row=6, column=0, pady=5)

    def calculate_deficit_surplus(self):

        consumed_calories = float(self.consumed_calories_entry.get())
        consumed_proteins = float(self.consumed_proteins_entry.get())
        consumed_fats = float(self.consumed_fats_entry.get())
        consumed_carbs = float(self.consumed_carbs_entry.get())

        if (consumed_calories != self.user_calories_norm or consumed_carbs != self.user_carbs or
                consumed_fats != self.user_fats or consumed_proteins != self.user_proteins):

            deficit_surplus_calories = round(((consumed_calories - self.user_calories_norm) / self.user_calories_norm) * 100)
            deficit_surplus_proteins = round(((consumed_proteins - self.user_proteins) / self.user_proteins) * 100)
            deficit_surplus_fats = round(((consumed_fats - self.user_fats) / self.user_fats) * 100)
            deficit_surplus_carbs = round(((consumed_carbs - self.user_carbs) / self.user_carbs) * 100)

            self.deficit_surplus_label.config(
                text=f"Deficit/Surplus:\n"
                     f"Calories: {deficit_surplus_calories}%\n"
                     f"Proteins: {deficit_surplus_proteins}%\n"
                     f"Fats: {deficit_surplus_fats}%\n"
                     f"Carbs: {deficit_surplus_carbs}%", fg="red"
             )
        else:
            self.deficit_surplus_label.config(text="You don`t have deficit or surplus", fg="red")

    def bodymass_index(self, mass, height):
        height_meters = height / 100
        bmi = mass / pow(height_meters, 2)
        return round(bmi, 1)

    def basalmet_rate(self, height, weight, gender, age):
        if gender == "Male":
            bmr = 88.362 + (13.397 * weight) + (4.779 * height) + (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.097 * height) + (4.33 * age)
        return bmr

    def calories_norm(self, bmr, act_coef):
        return bmr * act_coef

    def calculate_user_nutrition(self, average_calories_norm, goal):

        if goal == "lose":
            self.user_calories_norm = round(average_calories_norm * 0.8)
            self.user_proteins = round((self.user_calories_norm * 0.1) / 4)
            self.user_fats = round((self.user_calories_norm * 0.25) / 9)
            self.user_carbs = round((self.user_calories_norm * 0.7) / 4)
        elif goal == "maintain":
            self.user_calories_norm = average_calories_norm
            self.user_proteins = round((self.user_calories_norm * 0.10) / 4)
            self.user_fats = round((self.user_calories_norm * 0.3) / 9)
            self.user_carbs = round((self.user_calories_norm * 0.7) / 4)
        else:
            self.user_calories_norm = round(average_calories_norm * 1.2)
            self.user_proteins = round((self.user_calories_norm * 0.15) / 4)
            self.user_fats = round((self.user_calories_norm * 0.3) / 9)
            self.user_carbs = round((self.user_calories_norm * 0.75) / 4)

        return self.user_calories_norm, self.user_proteins, self.user_fats, self.user_carbs

    def open_table(self):
        main_table = Toplevel(self.main_calculator)
        table = CaloriesTable(main_table)

        try:
            with open("calories_table_data.json", "r") as file:
                table_data = json.load(file)
                table.load_table_data(table_data)
        except FileNotFoundError:
            pass

        main_table.mainloop()


class CaloriesTable:

    def __init__(self, root):
        self.root = root
        self.root.title("Nutrition Calculator")
        self.setup_table()

    def setup_table(self):

        self.table = ttk.Treeview(self.root, columns=("Product", "Calories", "Proteins", "Fats", "Carbs"),
                                  show="headings")
        self.table.pack(padx=10, pady=10)

        self.table.heading("Product", text="Product")
        self.table.heading("Calories", text="Calories")
        self.table.heading("Proteins", text="Proteins")
        self.table.heading("Fats", text="Fats")
        self.table.heading("Carbs", text="Carbs")

        self.table.pack(padx=10, pady=10)

        self.add_button = Button(self.root, text="Add Food Item", command=self.add_food)
        self.add_button.pack(pady=10)

        Label(self.root, text="Weight of the food item (g):").pack(pady=5)
        self.food_weight = Entry(self.root)
        self.food_weight.pack(pady=5)

        self.calculate_button = Button(self.root, text="Calculate", command=self.calculate_food_nutrition)
        self.calculate_button.pack(pady=10)

        self.result_label = Label(self.root, text="")
        self.result_label.pack(pady=5)

        self.exit_button = Button(self.root, text="Exit", command=self.exit_command)
        self.exit_button.pack(pady=10)

    def exit_command(self):
        table_data = self.get_table_data()
        with open("calories_table_data.json", "w") as file:
            json.dump(table_data, file)
        self.root.destroy()

    def get_table_data(self):
        table_data = []
        for item_id in self.table.get_children():
            values = self.table.item(item_id, 'values')
            table_data.append({
                "Product": values[0],
                "Calories": values[1],
                "Proteins": values[2],
                "Fats": values[3],
                "Carbs": values[4],
            })
        return table_data

    def load_table_data(self, table_data):
        for item in table_data:
            self.table.insert("", "end",
                              values=(item["Product"], item["Calories"], item["Proteins"], item["Fats"], item["Carbs"]))

    def add_food(self):
        food_window = Toplevel(self.root)
        food_window.title("Add Food Item")

        Label(food_window, text="Name of the food item:").grid(row=0, column=0, padx=10, pady=5)
        Label(food_window, text="Calories:").grid(row=1, column=0, padx=10, pady=5)
        Label(food_window, text="Proteins:").grid(row=2, column=0, padx=10, pady=5)
        Label(food_window, text="Fats:").grid(row=3, column=0, padx=10, pady=5)
        Label(food_window, text="Carbs:").grid(row=4, column=0, padx=10, pady=5)

        entry_name = Entry(food_window)
        entry_calories = Entry(food_window)
        entry_proteins = Entry(food_window)
        entry_fats = Entry(food_window)
        entry_carbs = Entry(food_window)

        entry_name.grid(row=0, column=1, padx=10, pady=5)
        entry_calories.grid(row=1, column=1, padx=10, pady=5)
        entry_proteins.grid(row=2, column=1, padx=10, pady=5)
        entry_fats.grid(row=3, column=1, padx=10, pady=5)
        entry_carbs.grid(row=4, column=1, padx=10, pady=5)

        def add_food_to_table():
            name = entry_name.get()
            calories = entry_calories.get()
            proteins = entry_proteins.get()
            fats = entry_fats.get()
            carbs = entry_carbs.get()

            self.table.insert("", "end", values=(name, calories, proteins, fats, carbs))

            food_window.destroy()

        add_button = Button(food_window, text="Add", command=add_food_to_table)
        add_button.grid(row=5, column=0, columnspan=2, pady=10)

    def calculate_food_nutrition(self):
        weight = self.food_weight.get()

        try:
            weight = float(weight)
        except ValueError:
            self.result_label.config(text="Please enter a valid weight.")
            return

        selected_item = self.table.selection()
        if not selected_item:
            self.result_label.config(text="Please select a product/food item.")
            return

        values = self.table.item(selected_item)['values']
        if not values:
            self.result_label.config(text="No nutrition data for the selected product/food item.")
            return

        result_calories = round((weight / 100) * float(values[1]), 2)
        result_proteins = round((weight / 100) * float(values[2]), 2)
        result_fats = round((weight / 100) * float(values[3]), 2)
        result_carbs = round((weight / 100) * float(values[4]), 2)

        result_text = (f"Nutrition for {values[0]} ({weight} g):\n"
                       f"Calories: {result_calories} kcal\n"
                       f"Proteins: {result_proteins} g\n"
                       f"Fats: {result_fats} g\n"
                       f"Carbs: {result_carbs} g")

        self.result_label.config(text=result_text)


if __name__ == "__main__":
    app = CalculatorApp()
    app.authoriz_window.mainloop()
