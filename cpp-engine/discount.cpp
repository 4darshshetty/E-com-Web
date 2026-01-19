#include "engine.h"

double applyDiscount(double price, int percent) {
    if (percent < 0 || percent > 70) return price;
    return price - (price * percent / 100.0);
}
