from numpy import *
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------------------------------------------------------------------------

#                               В ДВУХ ЭТИХ ФУНКЦИЯХ НУЖНО ПОМЕНЯТЬ КОЭФИЦЕНТЫ !!!

# Временной ряд
def F(k, C1 = 1, C2 = 2, M1 = 3, M2 = 4 , B1 = 1, B2 = 1, B3 = 1, B4 = 1): 
    Xp = (10 ** (-3)) * cos((B1 + B2 + B3 + B4) * k)
    E = exp( (10 ** (-5)) * (C1 + C2 + M1 + M2) * k )
    S = sin(k/(C1 + C2 + M1 + M2))
    return Xp + (E * S) 

# Запаздывание
def F_Delay(kPi = 0,C1 = 1, C2 = 2, M1 = 3, M2 = 4): return  kPi * pi * (C1 + C2 + M1 + M2) 

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Получаем массив значений функции по X и по Y
def RowGenerator(f,a=0,b=1,step = 0.1, kPi = 0): return [f(x) for x in arange(a - F_Delay(kPi),b - F_Delay(kPi), step)]

# --- Среднее значение ---
# --- Массив данных ---
def Average(Mass): return (sum(Mass) / len(Mass))

# --- Дисперсия ---
# ---Массив данных, Мат Ожидание ---
def Dispersion(Mass, Av):
    Ds = 0
    for i in Mass: Ds += (i - Av)**2
    return Ds / len(Mass)

# --- Отклонение ---
# --- Массив данных, Мат Ожидание ---
def DispOtkl(Mass, Av): return sqrt(Dispersion(Mass, Av))

# --- Сумма произведений двух массивов ---
# --- Первый массив данных, Второй массив данных ---
def SumMass(Mass_1,Mass_2):
    Sm = 0
    for i in range((len(Mass_1)+len(Mass_2))/2):
        Sm += Mass_1[i]*Mass_2[i]
    return Sm

# --- Корреляция ---
# --- Первый массив данных, Второй массив данных, Длина сдвига ---
def Correlation(Mass_1, Mass_2, Av1, Av2, T):
    Cr, N = 0, len(Mass_1)
    for i in range(N-T):
        Cr += (Mass_1[i]-Av1)*(Mass_2[i+T]-Av2)
    return Cr/(N-T)

# --- Коэффициент корреляции (ККФ) ---
# --- Первый массив данных, Второй массив данных, Мат ожидания и отклонения первого и второго сигнала Длина сдвига ---
def CoefCr(Mass_1, Mass_2, Av1, Av2, Ds1, Ds2, T):
    Cr = Correlation(Mass_1, Mass_2, Av1, Av2, T)
    return Cr/((Ds1)*(Ds2))

# --- Автокорреляционная функця (АКФ) ---
# --- Первый массив данных, Второй массив данных, Длина сдвига ---
def AutoCr(Mass_1, Mass_2, T):
    AKF = []
    Av1 = Average(Mass_1)
    Av2 = Average(Mass_2)
    Ds1 = DispOtkl(Mass_1, Av1)
    Ds2 = DispOtkl(Mass_2, Av1)
    for i in range(T):
        AKF.append(CoefCr(Mass_1, Mass_2, Av1, Av2, Ds1, Ds2, i))
    return AKF

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Стартер
def Start():

    X = arange(-100,100, 0.1)

    Signal_1 = RowGenerator(F,a=-100,b=100,step=0.1,kPi=0)
    Signal_2 = RowGenerator(F,a=-100,b=100,step=0.1,kPi=1)
    Signal_3 = RowGenerator(F,a=-100,b=100,step=0.1,kPi=2)

    plt.subplot(2,3,1); plt.plot(X,Signal_1,color="g"); plt.title("Сигнал временного ряда",fontsize=10)
    plt.subplot(2,3,2); plt.plot(X,Signal_2,color="r"); plt.title("Сигнал с запозданием на $Pi(C1+C2+M1+M2)$",fontsize=10)
    plt.subplot(2,3,3); plt.plot(X,Signal_3,color="b"); plt.title("Сигнал с запозданием на $2Pi(C1+C2+M1+M2)$",fontsize=10)
    
    plt.subplot(2,3,4); plt.plot(AutoCr(Signal_1,Signal_2,1000),color="g"); plt.title("Корреляция между первым и вторым сигналом",fontsize=10)
    plt.subplot(2,3,5); plt.plot(AutoCr(Signal_1,Signal_3,1000),color="r"); plt.title("Корреляция между первым и третьим сигналом",fontsize=10)
    plt.subplot(2,3,6); plt.plot(AutoCr(Signal_2,Signal_3,1000),color="b"); plt.title("Корреляция между вторым и третьим сигналом$",fontsize=10)
    
    plt.show()

# Главный метод
if __name__ == "__main__": Start()