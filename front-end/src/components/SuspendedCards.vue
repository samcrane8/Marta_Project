<template>
  <v-layout column>
    <v-flex xs12 class="text-xs-center" mt-5>
      <h3>Suspended Cards</h3>
    </v-flex>
    <v-card style="margin: 20px; padding: 5px;" flat>
	    <v-data-table
	        v-bind:headers="headers"
	        :items="items"
	        item-key="date_suspended"
	        hide-actions
	        class="elevation-1"
	      >
	      <template slot="items" slot-scope="props">
	      	<tr @click="props.expanded = !props.expanded">
		        <td>{{ props.item.card_id }}</td>
		        <td class="text-xs-center">{{ props.item.new_owner }}</td>
		        <td class="text-xs-center">{{ props.item.date_suspended }}</td>
		        <td class="text-xs-center">{{ props.item.old_owner }}</td>
	    	</tr>
	      </template>
	      <template slot="expand" slot-scope="props">
		  	<v-card>
		  		<v-card-title>
		          <h3 class="headline mb-0">Resolve Conflict</h3>
		        </v-card-title>
		        <v-card-actions>
			  		<v-layout row>
					    <v-flex>
				        	<v-btn flat color="blue" @click="props.expanded = false;assign_owner(props.item, false)">Assign to Old Owner</v-btn>
				        </v-flex>
				    	<v-flex class="text-xs-right">
				        	<v-btn flat color="blue" @click="props.expanded = false;assign_owner(props.item, true)">Assign to New Owner</v-btn>
				        </v-flex>
				    </v-layout>
				</v-card-actions>
			</v-card>
		  </template>
	    </v-data-table>
	    <v-card style="margin-top:20px;" flat>
	    	<v-card-text class="text-xs-center">
	    		Note: assigning the card to an owner will unlock all <br> accounts conflicted on the same Breeze Card.
	    	</v-card-text>
	    </v-card>
	</v-card>
  </v-layout>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import router from '@/router'
 
Vue.use(VueAxios, axios)

export default {
	data () {
	    return {
	      headers: [
	        {text: 'Card#', value: 'card_id', align: 'left'},
	        { text: 'New Owner', value: 'new_owner', align: 'center'},
	        { text: 'Date Suspended', value: 'date_suspended', align: 'center'},
	        { text: 'Old Owner', value: 'old_owner', align: 'center'}
	      ],
	      items: []
	    }
	},
	methods: {
		refresh_conflicts() {
    		//now this is going to be run when they mount.
	    	var url = "http://54.173.144.94:5000/get_conflicts"
	    	axios.get(url)
		        .then((response) => {
		          this.items = response.data
		        })
		        .catch(error => {
		          alert('Hmmm something went wrong with our servers when fetching stations!! Sorry!')
		      });
    	},
    	assign_owner(item, resolve_to_new) {
    		var url = "http://54.173.144.94:5000/resolve_conflict"
    		var body = {
						"card_id" : item.card_id,
						"uname" : item.new_owner,
						"resolve_to_new" : resolve_to_new
					}
	    	axios.post(url, body)
		        .then((response) => {
    			  this.refresh_conflicts()
		        })
		        .catch(error => {
		          alert('Hmmm something went wrong with our servers when fetching stations!! Sorry!')
		      });
    	}
	},
    beforeMount(){
      this.refresh_conflicts()
    }
}
</script>