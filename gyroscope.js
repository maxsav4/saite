// Простая реализация параллакса фона при наклоне телефона (гироскоп)

const canvasBg = document.getElementById('liquid-bg');

// Проверяем поддержку событий ориентации устройства
if (window.DeviceOrientationEvent) {
    window.addEventListener('deviceorientation', function(event) {
        // alpha: вращение вокруг оси Z (0-360)
        // beta: наклон вперед-назад (-180-180)
        // gamma: наклон влево-вправо (-90-90)

        // Получаем значения наклона (ограничиваем для мягкости)
        let tiltX = Math.round(event.gamma); // Влево-Вправо
        let tiltY = Math.round(event.beta);  // Вперед-Назад

        // Вычисляем сдвиг (не более 15 пикселей)
        let moveX = (tiltX / 6); 
        let moveY = (tiltY / 6);

        // Применяем сдвиг к canvas с помощью трансформации
        // Использование translate3D задействует аппаратное ускорение
        canvasBg.style.transform = `translate3d(${moveX}px, ${moveY}px, 0) scale(1.1)`; 
        // scale(1.1) нужен, чтобы при сдвиге не было видно белых краев
    }, true);
}
