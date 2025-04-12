const express = require('express');
const path = require('path');

const app = express();
app.use(express.urlencoded({ extended: true }));
app.set('view engine', 'ejs');                      // Use EJS
app.set('views', path.join(__dirname, '../views')); // Adjust path if needed

app.use(express.static(path.join(__dirname, '../public')));

app.get('/', (req, res) => {
    res.render("index")
});


app.post('/results', (req, res) => {
    const mood = req.body.moodInput 
    const numSongs = req.body.numSongs 
    const genreType = req.body.genreType 
    console.log(mood)
    res.send("HI")
})

// app.post('/res', (req, res)) {
//     const mood = req.body.mood; 
//     console.log('User mood is: ' + mood) 

// }

// app.get('/results', (req,res) => {
//     res.render('results')
// });

app.listen(3000, console.log("working!"))