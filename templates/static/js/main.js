// get Stripe publishable key
fetch("/config/")
	.then((result) => { return result.json(); })
	.then((data) => {
		// initialize Stripe.js
		const stripe = Stripe(data.publicKey);

		// button click event handler
		document.querySelector("#comprar").addEventListener("click", () => {
			// Get Session ID
			fetch("/create-checkout-session/")
				.then((result) => { return  result.json(); })
				.then((data) => {

					// console.log(data);
					// Redirect to Stripe Checkout
					return stripe.redirectToCheckout({sessionId: data.sessionId})
				})
				.then((res) => {
					console.log(res);
				});
		});
	});
