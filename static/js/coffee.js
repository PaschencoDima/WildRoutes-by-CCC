// Входной JSON
const data = {
    "cafes": [
        { "name": "BolsheCoffee", "rating": 4.9, "description": "Кофе в гроте.", "coords": [59.955, 30.331], "menu": ["1", "2", "6"] },
        { "name": "ТЧК", "rating": 4.9, "description": "Уютный дворик.", "coords": [59.958, 30.302], "menu": ["6", "5", "1"] },
        { "name": "Характер Кофе", "rating": 4.8, "description": "На набережной.", "coords": [59.932, 30.342], "menu": ["3", "2", "4"] },
        { "name": "Civil", "rating": 4.7, "description": "Бертгольд Центр.", "coords": [59.928, 30.323], "menu": ["4", "3", "5"] },
        { "name": "Verle Garden", "rating": 4.8, "description": "Минимализм.", "coords": [59.959, 30.316], "menu": ["6", "1", "5"] },
        { "name": "Coffee 3", "rating": 4.8, "description": "Панорамный вид.", "coords": [59.972, 30.321], "menu": ["2", "6", "4"] },
        { "name": "Sibaristica", "rating": 4.9, "description": "Школа бариста.", "coords": [59.912, 30.278], "menu": ["1", "4", "3"] },
        { "name": "Mad Espresso", "rating": 4.7, "description": "Серьезный подход.", "coords": [59.938, 30.360], "menu": ["1", "2", "5"] },
        { "name": "STIM", "rating": 4.7, "description": "Кофе и сырники.", "coords": [59.926, 30.318], "menu": ["6", "3", "4"] },
        { "name": "Микро ТЧК", "rating": 4.8, "description": "Спешелти зерно.", "coords": [59.941, 30.352], "menu": ["1", "6", "2"] },
        { "name": "Обычные люди", "rating": 4.6, "description": "На каждый день.", "coords": [59.929, 30.362], "menu": ["3", "4", "1"] },
        { "name": "Cup", "rating": 4.8, "description": "Маленькая точка.", "coords": [59.931, 30.353], "menu": ["5", "6", "2"] },
        { "name": "Doris Local", "rating": 4.7, "description": "Для своих.", "coords": [59.961, 30.308], "menu": ["3", "2", "4"] },
        { "name": "Займемся кофе", "rating": 4.5, "description": "С характером.", "coords": [59.943, 30.334], "menu": ["4", "5", "3"] },
        { "name": "Smena", "rating": 4.9, "description": "Завтраки и кофе.", "coords": [59.945, 30.344], "menu": ["1", "6", "5"] },
        { "name": "Solaris Lab", "rating": 4.7, "description": "Кофе под куполом.", "coords": [59.925, 30.296], "menu": ["2", "3", "4"] },
        { "name": "Gotcha Brew Bar", "rating": 4.8, "description": "Альтернатива.", "coords": [59.927, 30.345], "menu": ["6", "1", "2"] },
        { "name": "Фильтр", "rating": 4.6, "description": "Просто фильтр.", "coords": [59.935, 30.325], "menu": ["4", "3", "5"] },
        { "name": "Sokol Coffee", "rating": 4.5, "description": "Портреты на кофе.", "coords": [59.933, 30.315], "menu": ["2", "1", "6"] },
        { "name": "Espresso Tonic", "rating": 4.4, "description": "Освежающий вкус.", "coords": [59.940, 30.280], "menu": ["3", "4", "5"] }
    ]
};

//const staticImagesPath = "{{ url_for('static', filename='images/') }}"
// Описания и картинки для видов кофе (имитация базы данных)
const coffeeDetails = {
    "1": { name: "Эспрессо", img: "/static/images/coffee/1.jpg", desc: "Классический крепкий кофе." },
    "2": { name: "Капучино", img: "/static/images/coffee/2.jpg", desc: "Нежная молочная пенка и эспрессо." },
    "3": { name: "Раф", img: "/static/images/coffee/3.jpg", desc: "Сливочный вкус и ванильный аромат." },
    "4": { name: "Латте", img: "/static/images/coffee/4.jpg", desc: "Много молока, мало кофе." },
    "5": { name: "Флэт Уайт", img: "/static/images/coffee/5.jpg", desc: "Насыщенный молочный вкус." },
    "6": { name: "Фильтр-кофе", img: "/static/images/coffee/6.jpg", desc: "Чистый вкус кофейного зерна." }
};

let myMap;
const placemarks = [];
const modal = new bootstrap.Modal(document.getElementById('cafeListModal'));

ymaps.ready(init);

function init() {
    myMap = new ymaps.Map("map", {
        center: [59.9386, 30.3141], // Питер
        zoom: 12
    });

    renderCoffeeCards();
    renderMarkers();

    myMap.setBounds(myMap.geoObjects.getBounds(), { checkZoomRange: true, zoomMargin: 50 });
}

function renderCoffeeCards() {
    const container = document.getElementById('coffee-container');

    const allCoffeeTypes = [...new Set(data.cafes.flatMap(cafe => cafe.menu))];

    allCoffeeTypes.forEach(code => {
        const info = coffeeDetails[code] || { name: "Кофе", img: "", desc: "Вкусный кофе." };
        const cardHtml = `
            <div class="col">
                <div class="card h-100 coffee-card" data-bs-theme="dark">
                    <img src="${info.img}" class="card-img-top" alt="${info.name}">
                    <div class="card-body">
                        <h5 class="card-title">${info.name}</h5>
                        <p class="card-text text-muted small">${info.desc}</p>

                        <div class="d-flex gap-2">
                            <button class="btn btn-coffee flex-fill btn-accent" onclick="highlightCafes('${code}')">
                                <i class="fa-solid fa-location-dot me-2"></i> На карте
                            </button>
                            <button class="btn btn-outline-dark flex-fill btn-sm btn-accent" onclick="showCafeList('${code}')">Список</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        container.innerHTML += cardHtml;
    });
}

function renderMarkers() {
    data.cafes.forEach(cafe => {
        const coffeeBadges = cafe.menu.map(item =>
            `<span class="badge bg-light text-dark border me-1">${coffeeDetails[item].name}</span>`
        ).join('');

        const placemark = new ymaps.Placemark(cafe.coords, {
            balloonContent: `
                <div class="p-2" style="min-width: 200px;">
                    <h5 class="mb-1 fw-bold text-dark">${cafe.name}</h5>
                    <div class="mb-2 text-warning">
                        <i class="fa-solid fa-star"></i> <strong>${cafe.rating}</strong>
                    </div>
                    <p class="small text-muted mb-2">${cafe.description}</p>
                    <div class="mt-2 text-dark">
                        <div class="small fw-bold mb-1">В меню:</div>
                        ${coffeeBadges}
                    </div>
                </div>`
        }, {
            iconLayout: 'default#imageWithContent',
            iconImageHref: '',
            iconImageSize: [40, 40],
            iconImageOffset: [-20, -20],
            iconContentLayout: ymaps.templateLayoutFactory.createClass(
                `<div class="custom-marker" style="
                    background: $[properties.iconColor];
                    width: 40px; height: 40px;
                    border-radius: 50%; border: 3px solid white;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.3);
                    display: flex; align-items: center; justify-content: center;
                    color: white; transition: all 0.3s;">
                    <i class="fa-solid fa-mug-hot" style="font-size: 18px;"></i>
                </div>`
            )
        });

        // Начальный цвет — серый
        placemark.properties.set('iconColor', '#6c757d');
        placemark.menu = cafe.menu;
        placemark.cafeData = cafe;
        placemarks.push(placemark);
        myMap.geoObjects.add(placemark);
    });
}

function highlightCafes(selectedCoffee) {
    placemarks.forEach(m => {
        const isPresent = m.menu.includes(selectedCoffee);
        m.properties.set('iconColor', isPresent ? '#ffc107' : '#6c757d');
        m.options.set('zIndex', isPresent ? 1000 : 1);
    });
    document.getElementById('map').scrollIntoView({ behavior: 'smooth' });
}

function showCafeList(code) {
    const cafes = data.cafes.filter(c => c.menu.includes(code));
    const listHtml = cafes.map(c => `
        <div class="list-group-item cafe-item p-3" onclick="focusCafe('${c.name}', '${code}')">
            <div class="d-flex justify-content-between align-items-center">
                <h6 class="mb-1 fw-bold">${c.name}</h6>
                <span class="badge bg-warning text-dark"><i class="fa-solid fa-star"></i> ${c.rating}</span>
            </div>
            <p class="small text-muted mb-0">${c.description}</p>
        </div>
    `).join('');

    document.getElementById('modalTitle').innerText = `Где подают ${coffeeDetails[code].name}`;
    document.getElementById('modalCafeList').innerHTML = listHtml;
    modal.show();
}

function focusCafe(cafe, code) {
    modal.hide();
    highlightCafes(code);
    const marker = placemarks.find(m => m.cafeData.name === cafe);
    if (marker) {
        myMap.setCenter(marker.geometry.getCoordinates(), 16, { duration: 500 });
        marker.balloon.open();
    }
}