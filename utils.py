from aiogram.dispatcher.filters.state import State, StatesGroup

class State(StatesGroup):
    menuState = State()
    communicationState = State()
    catalogState = State()
    orderState = State()
    cancelState = State()
    buyState = State()

    documentState = State()
    licensePhoto = State()
    certificatesPhoto = State()

    modelCar = State()
    carStock = State()
    rightNow = State()
    
    adminState = State()
    modelCarAdmin = State()

    rangeState = State()
    toyotaState = State()
    lexusState = State()
    chevroletState = State()
    kiaState = State()
    mercedesState = State()
    hyundaiState = State()
    mitsubishiState = State()
    
if __name__ == '__main__':
    print(State.all())