const socket = io();
//        
//"name": self.name,
//"id": self.id,
//"author": self.author,
//"difficulty": self.difficulty,
//"downloads": self.downloads,
//"likes": self.likes,
//"length": self.length,
//"stars": self.stars,
//"coins": self.coins,
//"difficultyFace": self.difficultyFace,
//"songName": self.songName,
//"userName" : self.UserName,
//"userAvatarURL": self.UserAvatarURL
//        

var i = 0;
var original = document.getElementById('Template');
const MissingText = document.getElementById('MissTXT')

function duplicate(data) {
    MissingText.style.display = 'none'
    const DataOBJ = data
    var original = document.getElementById('Template'); // O elemento original que será clonado
    var clone = original.cloneNode(true); // "deep" clone
    clone.id = "Template" + ++i; // Define um ID único para o clone
    const nameElement = clone.querySelector('.NumInList');
    if (nameElement) {
        nameElement.textContent = `${i}º`; // muda o texto, por exemplo
    }
    // Atualiza os IDs e classes dos filhos do clone
    var elements = clone.querySelectorAll('[id], [class]'); // Seleciona elementos com ID ou classe
    original.parentNode.appendChild(clone);
    clone.style.display = "flex"
    elements.forEach((element, index) => {
        // Atualiza o ID, se existir
        if (element.id) {
            element.id = `Level${i+1}`;
        }
        
        
        if (i % 2 == 0){
                clone.style.background = '#C1743F'
        }
    })

    function changeText(text,className) {
        clone.querySelector(`.${className}`).textContent = text
    }
    function popCoin(coin){
        clone.querySelector(`.coin${coin}`).style.display = "none"
    }
    clone.querySelector('.DifFace').src = ` https://gdbrowser.com/assets/difficulties/${DataOBJ.difficultyFace}.png`
    clone.querySelector('.RequesterImage').src = DataOBJ.userAvatarURL

    changeText(DataOBJ.difficulty, 'DifName')
    changeText(DataOBJ.stars, 'StarsNumber')
    changeText(DataOBJ.name, 'Name')
    changeText(DataOBJ.author, 'Author')
    changeText(DataOBJ.songName, 'Song')
    changeText(DataOBJ.length, 'Time')
    changeText(DataOBJ.downloads, 'Downloads')
    changeText(DataOBJ.likes, 'Likes')
    changeText(DataOBJ.userName, 'Requester')
    changeText(DataOBJ.id, 'LevelId')
    if (DataOBJ.stars === 0){
        clone.querySelector('.Stars').style.display = "none"
    }
    if(DataOBJ.coins ===2 ){
        popCoin(3)
    } else if (DataOBJ.coins ===1 ){
        popCoin(3)
        popCoin(2)
    } else if (DataOBJ.coins ===0 ){
        popCoin(3)
        popCoin(2)
        popCoin(1)
    }






    // Adiciona o clone ao DOM
    
}

socket.on("Reset", (data) => {
    console.log('Reiniciando DOM')
    location.reload()
})

socket.on("AddLevel", (data) => {
    console.log(data)
    duplicate(data)
    

});

socket.on("RemoveLevel", (number) => {
    console.log("Removendo Template", number);

    // Remove o elemento
    const deletavel = document.getElementById(`Template${number}`);
    if (deletavel) {
        deletavel.remove();
    }

    // Reordena os IDs dos elementos restantes
    const levelsContainer = document.getElementById("Main");
    const templates = levelsContainer.querySelectorAll("[id^='Template']");

    templates.forEach((element, index) => {
        if (element.id != 'Template'){
            console.log(element.id,index)
            element.id = `Template${index}`;
            element.querySelector('.NumInList').textContent = `${index}º`
            
            
            
            if (index % 2 == 0){
                element.style.background = '#C1743F'
            } else {
                element.style.background = "#A1582C"
            }
        }
    });
    i--
    if (i === 0){
        MissingText.style.display = 'block'
    }
});