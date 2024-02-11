let pageNumber = 1;
let lastPage = 1;
let sourceArray = [];
let resultArray = [];
var selectedImages = [];
let selectedImagesData = []; // 이미지 데이터를 저장할 배열

const fileNameElement = document.querySelector('#file-name');

function prePage() {
    if (pageNumber == 1) {
        alert("첫 페이지 입니다");
    } else {
        pageNumber -= 1;
        document.querySelector('.source-image').src = "../static/uploads/source" + pageNumber + ".png"
        document.querySelector('.result-image').src = "../static/uploads/result" + pageNumber + ".png"
        document.querySelector('#file-name').textContent = pageNumber;
    }
}

function nextPage() {
    if (pageNumber == resultArray.length) {
        alert("마지막 이미지입니다.");
    } else {
        pageNumber += 1;
        document.querySelector('.source-image').src = "../static/uploads/source" + pageNumber + ".png"
        document.querySelector('.result-image').src = "../static/uploads/result" + pageNumber + ".png"
        document.querySelector('#file-name').textContent = pageNumber;
    }
}

function submitImage() {
    // 이미지 제출 로직을 여기에 추가합니다.
    document.getElementById("image-upload").click();
}

function handleImageUpload(event) {
    // 사용자가 이미지를 선택하면 호출되는 함수
    var imageFiles = event.target.files;
    selectedImages = Array.from(imageFiles); // 선택한 이미지들을 배열에 저장

    // .rectangle 태그를 display=none으로 변경합니다.
    var rectangle = document.querySelector(".rectangle");
    rectangle.style.display = "none";

    document.querySelector(".source-image").style.display = "block";
    document.querySelector(".result-image").style.display = "block";

    deleteImages();
    uploadImages();

}

const deleteImages = () => {
    fetch('/image-delete', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
        })
        .catch((error) => {
            console.error(error);
        });
}


function uploadImages() {
    sourceArray = [];
    resultArray = [];
    // 선택한 이미지들을 서버로 업로드하는 함수
    for (var i = 0; i < selectedImages.length; i++) {
        var imageFile = selectedImages[i];
        var filename = "source" + (i + 1) + ".png"; // 이미지 파일명을 지정

        // FormData 객체를 생성하여 이미지 파일을 담습니다.
        var formData = new FormData();
        formData.append('file', imageFile, filename); // 파일명을 추가로 지정

        // 서버 업로드 URL을 지정합니다.
        var uploadUrl = '/upload';

        // AJAX 요청을 보냅니다.
        fetch(uploadUrl, {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                // 서버 응답 처리
                console.log('Uploaded file:', data.uploaded_files);
                sourceArray.push("../static/uploads/source" + i + ".png");
                resultArray.push("../static/uploads/result" + i + ".png");

                document.querySelector('.source-image').src = "../static/uploads/source1.png"
                document.querySelector('.result-image').src = "../static/uploads/result1.png"
                document.querySelector('#file-name').textContent = pageNumber;
            })
            .catch(error => {
                console.error('Error uploading file:', error);
            });
    }

}

function toggleImageDisplay() {
    var checkbox = document.getElementById("checkbox");
    var resultImage = document.querySelector(".result-image");
    var sourceImage = document.querySelector(".source-image");

    resultImage.style.filter = "brightness(1) sepia(100%) saturate(10000%) hue-rotate(0deg)";

    if (checkbox.checked) {
        resultImage.style.opacity = "0.5";
        resultImage.style.display = "block";
    } else {
        resultImage.style.display = "none";
        sourceImage.style.display = "block";
    }

}