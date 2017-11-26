<template>
  <v-layout column>
	<v-flex xs12 class="text-xs-center" mt-5>
	  <h3>Welcome Aboard!</h3>
	</v-flex>
	<v-flex class="text-xs-center" mt-5 style = "margin: 20px;">
	  <p>Hey Passenger! Get ready for the fastest, slickest marta experience. All you have to do is login now with your new passenger account. Would you like to go to the login page?</p>
	</v-flex>
		<v-flex class="text-xs-center" mt-5>
		  <v-btn flat primary to="/signin">Log In</v-btn>
		</v-flex>
  </v-layout>
</template>

<script>
export default {}
</script>