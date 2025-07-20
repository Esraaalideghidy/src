
//الكود دا لصفحه الكارد عشان يزود علي طول
var updateBtns = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function () {
		let productId = this.dataset.product;
		let action = this.dataset.action;

		// نحاول ناخد اللون والمقاس من الزر أولًا
		let selectedColor = this.dataset.color || null;
		let selectedSize = this.dataset.size || null;

		// لو مش موجودين، نحاول نجيبهم من الفورم
		if (!selectedColor || !selectedSize) {
			let productElement = this.closest('.product-data');
			if (productElement) {
				let colorInput = productElement.querySelector('[name="color"]');
				let sizeInput = productElement.querySelector('[name="size"]');

				if (colorInput) selectedColor = colorInput.value;
				if (sizeInput) selectedSize = sizeInput.value;
			}
		}

		console.log('Product ID:', productId, 'Action:', action, 'Color:', selectedColor, 'Size:', selectedSize);

		if (user === 'AnonymousUser') {
			addCookieItem(productId, action, 1, selectedColor, selectedSize);
		} else {
			updateUserOrder(productId, action, 1, selectedColor, selectedSize);
		}
	});
}

//الكود دا لصفحه تفاصيل البرودكت عشان احدد الكميه الاول وبعدين اعمل اضافه للكارد
var addToCartBtns = document.getElementsByClassName('add-to-cart-btn');

for (let i = 0; i < addToCartBtns.length; i++) {
	addToCartBtns[i].addEventListener('click', function () {
		const productId = this.dataset.product;
		const qtyInput = document.getElementById('qty-' + productId);
		const quantity = parseInt(qtyInput.value) || 1;

		// if (user === 'AnonymousUser') {
		// 	alert('You must login first');
		// 	return;
		// }
		const selectedColor = document.getElementById('colorSelect').value;
		const selectedSize = document.getElementById('sizeSelect').value;
		if (selectedColor === "" || selectedSize === "") {
		alert("Please select both color and size before adding to cart.");
		return;
		}

		if (user === 'AnonymousUser') {
			addCookieItem(productId, 'add', quantity, selectedColor, selectedSize);
		} else {
			updateUserOrder(productId, 'add', quantity, selectedColor, selectedSize);
		}

		
		qtyInput.value = 1;  // Reset to 1 after adding to cart
	});
}

function addCookieItem(productId, action,quantity = 1,selectedColor = null, selectedSize = null) {
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined) {
			cart[productId] = {'quantity': quantity,
				'color': selectedColor,
				'size': selectedSize
			};
		} else {
			cart[productId]['quantity'] += quantity;
			if (selectedColor) {
				cart[productId]['color'] = selectedColor;
			}
			if (selectedSize) {
				cart[productId]['size'] = selectedSize;
			}
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	location.reload()
}
function updateUserOrder(productId, action, quantity = null ,selectedColor = null, selectedSize = null) {
	console.log('User is authenticated, sending data...');

	const url = '/cart/update_item/';

	if (quantity === null || isNaN(quantity) || quantity <= 0) {
		quantity = 1;
	}

	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({
			'productId': productId,
			'action': action,
			'quantity': quantity,
			'color': selectedColor,
			'size': selectedSize
		})
	})
	.then(response => response.json())
	.then(data => {
		console.log('Response:', data);
		location.reload();
	});
}
//ودا تبع الكود بتاع صفحه تفاصيل العنصر عشان زياده ونقصان 
let increaseBtns = document.getElementsByClassName('increase');
let decreaseBtns = document.getElementsByClassName('reduced');

for (let i = 0; i < increaseBtns.length; i++) {
	increaseBtns[i].addEventListener('click', function () {
		let productId = this.dataset.product;
		let input = document.getElementById('qty-' + productId);
		let qty = parseInt(input.value) || 1;
		input.value = qty + 1;
	});
}

for (let i = 0; i < decreaseBtns.length; i++) {
	decreaseBtns[i].addEventListener('click', function () {
		let productId = this.dataset.product;
		let input = document.getElementById('qty-' + productId);
		let qty = parseInt(input.value) || 1;
		if (qty > 1) {
			input.value = qty - 1;
		}
	});
}
// حذف نهائي للمنتج من السلة
let deleteBtns = document.getElementsByClassName('delete-item-btn');

for (let i = 0; i < deleteBtns.length; i++) {
	deleteBtns[i].addEventListener('click', function () {
		let productId = this.dataset.product;
		let quantity = parseInt(this.dataset.quantity) || 1;
		let selectedColor = this.dataset.color || null;
		let selectedSize = this.dataset.size || null;

		if (user === 'AnonymousUser') {
			// حذف من الكوكيز
			if (cart[productId] !== undefined) {
				delete cart[productId];
				document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
				location.reload();
			}
		} else {
			// إرسال كمية تساوي الكمية الموجودة فعلاً
			updateUserOrder(productId, 'delete', quantity, selectedColor, selectedSize);

		}
	});
}

