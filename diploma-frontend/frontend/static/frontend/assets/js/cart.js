var mix = {
    methods: {
        confirmOrder() {
        if (!this.name || !this.number1 || !this.month || !this.year || this.code) {
            alert('Пожалуйста, заполните все необходимые поля.');
            return;
        }

        const orderData = {
            name: this.name,
            number: this.number1,
            year: this.year,
            month: this.month,
            code: this.code,
            basket: Object.values(this.basket),
        };

        this.postData('/api/confirm_order', orderData)
            .then(response => {
                console.log(response);
            })
            .catch(error => {
                console.error(error);
            });
        },
    },
    mounted() {},
    data() {
        return {}
    }
}