import re
from consolemenu import *
from consolemenu.items import *
from ConvenienceFunctions import is_not_integer, make_ordinal, is_not_one_or_two
from EditScheduleMenuMethods import deleteTripOffering, addTripOfferings, changeDriver, changeBus
from MainMenuMethods import displaySchedule, displayStops, displayDriverSchedule, addDriver, addBus, deleteBus, insertActualTrip
from DatabaseInitialization import initializeDatabase

def main():
    # initialize our database and create its tables
    initializeDatabase()
    print("Database initialized Successfully")

    # create a menu with options
    menu = ConsoleMenu("Main Menu")
    function_item1 = FunctionItem(
        "Display the schedule of all trips for a given start location, destination, and date.", displaySchedule)

    function_item2 = FunctionItem(
        "Display the stops of a given trip.", displayStops)

    function_item3 = FunctionItem(
        "Display the weekly schedule of a given driver and date.", displayDriverSchedule)

    function_item4 = FunctionItem(
        "Add a driver.", addDriver)

    function_item5 = FunctionItem(
        "Add a bus.", addBus)

    function_item6 = FunctionItem(
        "Delete a bus.", deleteBus)

    function_item7 = FunctionItem(
        "Insert data for an actual trip specified by its key.", insertActualTrip)

    editScheduleSubmenu = ConsoleMenu("Edit Schedules")
    editScheduleOption1 = FunctionItem("Delete a trip offering by TripNumber, Date, and Scheduled Start Time.",
                                       deleteTripOffering)

    editScheduleOption2 = FunctionItem(
        "Add a set of Trip Offerings.", addTripOfferings)

    editScheduleOption3 = FunctionItem("Change the driver for a given Trip Offering.", changeDriver)
    editScheduleOption4 = FunctionItem("Change the bus for a given Trip Offering.", changeBus)

    editScheduleSubmenu.append_item(editScheduleOption1)
    editScheduleSubmenu.append_item(editScheduleOption2)
    editScheduleSubmenu.append_item(editScheduleOption3)
    editScheduleSubmenu.append_item(editScheduleOption4)

    submenu_item_1 = SubmenuItem("Edit Schedules", submenu=editScheduleSubmenu)
    submenu_item_1.set_menu(menu)

    menu.append_item(function_item1)
    menu.append_item(submenu_item_1)
    menu.append_item(function_item2)
    menu.append_item(function_item3)
    menu.append_item(function_item4)
    menu.append_item(function_item5)
    menu.append_item(function_item6)
    menu.append_item(function_item7)
    menu.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
