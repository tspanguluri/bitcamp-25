const express = require('express');
const path = require('path');
const axios = require('axios')
const app = express();
app.use(express.urlencoded({ extended: true }));
app.set('view engine', 'ejs');                      // Use EJS
app.set('views', path.join(__dirname, '../views')); // Adjust path if needed

app.use(express.static(path.join(__dirname, '../public')));

app.get('/', (req, res) => {
    res.render("index")
});


app.post('/results', async (req, res) => {
    const mood = req.body.moodInput 
    const song_num = req.body.numSongs 
    const genres = req.body.genreType 
    try {
        const response = await axios.get('http://localhost:8000/chatgpt/chatgpt', {
            params: {
                "mood": mood, 
                "song_num": song_num, 
                "genres": genres 
            }
        });
        const results = response.data
        const songs = results.songs 
        res.render("results", {songs})
    } catch (error) {
        console.log(error)
    }
    
})

// app.post('/res', (req, res)) {
//     const mood = req.body.mood; 
//     console.log('User mood is: ' + mood) 

// }

// app.get('/results', (req,res) => {
//     res.render('results')
// });

app.listen(3000, console.log("working!"))