import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [

  { path: '/', component: 'Landing' },
  { path: '/signin', component: 'Signin' },
  { path: '/signup', component: 'Signup' },
  { path: '/career', component: 'Career'},
  { path: '/company', component: 'Company'},
  { path: '/pricing', component: 'Pricing'},
  { path: '/welcomeuser', component: 'WelcomeUser'},
  { path: '/logout', component: 'Logout'},

  { path: '/admindashboard', component: 'AdminDashboard'},
  { path: '/stationmanagement', component: 'StationManagement'},
  { path: '/suspendedcards', component: 'SuspendedCards'},
  { path: '/breezecardmanagement', component: 'BreezeCardManagement'},
  { path: '/passengerflowreport', component: 'PassengerFlowReport'},

  { path: '/manageuserbreezecards', component: 'ManageBreezecards'},
  { path: '/managetrips', component: 'ManageTrips'},
  { path: '/passengerdashboard', component: 'PassengerDashboard'},
  { path: '/triphistory', component: 'TripHistory'}
]

const routes = routerOptions.map(route => {
  return {
    path: route.path,
    component: () => import(`@/components/${route.component}.vue`),
    props: true
  }
})

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes
})