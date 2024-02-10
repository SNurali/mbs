var mix = {
	methods: {
		getOrder(orderId) {
			...
		},
        confirmOrder() {
            if (this.orderId !== null) {
                const orderData = {
                    fullName: this.fullName,
                    phone: this.phone,
                    email: this.email,
                    deliveryType: this.deliveryType,
                    city: this.city,
                    address: this.address,
                    paymentType: this.paymentType,
                    products: this.products,
                };

                this.postData(`/api/order/${this.orderId}`, orderData)
                    .then(({data: {orderId}}) => {
                        alert('Заказ подтвержден');
                        // Если выбран вариант "Оплата при получении", переходим на страницу заказа
                        if (this.paymentType === 'cashOnDelivery'){
                            location.replace(`/orders/${this.orderId}/`);
                        } else{
                            // Иначе осуществляем переход на страницу оплаты
                            location.replace(`/payment/${this.orderId}/`);
                        }
                    })
                    .catch(() => {
                        console.warn('Ошибка при подтверждения заказа')
                    })
            }
        },
		...
	},
	mounted() {
		...
	},
	data() {
		return {
			orderId: null,
			createdAt: null,
			fullName: null,
			phone: null,
			email: null,
			deliveryType: null,
			city: null,
			address: null,
			paymentType: null,
			status: null,
			totalCost: null,
			products: [],
		}
	},
}