# Математическая модель

Качка платформы:

```text
theta_platform(t) = A * cos(Omega * t + phi0)
Omega = 2*pi / T
```

Начальные условия:

```text
theta0 = A * cos(phi0)
omega0 = -A * Omega * sin(phi0)
```

Система для RK2:

```text
y'     = v(t) * sin(theta)
theta' = omega
omega' = -a * theta(t - tau)
```

Sweep:

```text
phi0_i = 2*pi*i/N
Delta_y_max = max_i |Delta_y_i|
```
