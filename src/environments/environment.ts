// This file can be replaced during build by using the `fileReplacements` array.
// `ng build ---prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  production: false,
  config : {
    apiKey: "AIzaSyArWdzKfzAH9zpkE2SMsBkvIR7Om8qyLE8",
    authDomain: "tiago-ihouse.firebaseapp.com",
    databaseURL: "https://tiago-ihouse.firebaseio.com",
    projectId: "tiago-ihouse",
    storageBucket: "tiago-ihouse.appspot.com",
    messagingSenderId: "984665681454"
  }
};

/*
 * In development mode, to ignore zone related error stack frames such as
 * `zone.run`, `zoneDelegate.invokeTask` for easier debugging, you can
 * import the following file, but please comment it out in production mode
 * because it will have performance impact when throw error
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.
