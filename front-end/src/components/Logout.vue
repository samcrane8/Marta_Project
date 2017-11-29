<template>
  <v-layout column>
	<v-flex xs12 class="text-xs-center" mt-5>
	  <h3>Logging Out</h3>
	</v-flex>
	<v-flex class="text-xs-center" mt-5 style = "margin: 20px;">
	  <p>Are you sure you want to logout?</p>
	</v-flex>
		<v-layout row justify-center>
			<v-flex class="text-xs-center" mt-5>
			  <v-btn flat primary @click.prevent="logout">YES</v-btn>
			</v-flex>
		</v-layout>
  </v-layout>
</template>

<script>
import router from '@/router'

export default {
	methods: {
		logout() {
			this.$emit('logout')
		}
	}
}
</script>