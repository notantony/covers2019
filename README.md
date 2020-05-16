# Child repositories
[Cropping & composition server](https://github.com/notantony/Grid-Anchor-based-Image-Cropping-Pytorch) \
[Semantic segmentation server](https://github.com/notantony/semantic-segmentation-pytorch)

# API

## Object detection
Object detection via Google Cloud.

#### Input:
Address: `/detection`, POST \
MIMEs: `applcation/json`, `image/jpeg`, `image/png`

Parameters when json: \
`data`: base64-encoded image. \
`type`: optional, image extension. Can be omitted for most of extensions.

#### Output:
List of detected objects. \
For each object: \
`name`: recognized object \
`score`: confidence in range [0, 1] \
`box`: 4-element list of coordinates of the object, clockwise, starting from the top left corner. <b> Coordinates are floating-point proportions in range [0, 1]. </b> 


<details>
  <summary> <b>Sample: </b> </summary> 

  Request JSON:
  ```json
  {
      "data": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxM...",
      "type": "jpeg"
  }
  ```
  
  Response:
  ```json
  [
      {
          "box": [
              [ 0.5293645262718201, 0.06992649286985397 ],
              [ 0.9699668288230896, 0.06992649286985397 ],
              [ 0.9699668288230896, 0.9906497597694397 ],
              [ 0.5293645262718201, 0.9906497597694397 ]
          ],
          "name": "Cat",
          "score": 0.9038124680519104
      },
      {
          "box": [
              [ 0.06010574474930763, 0 ],
              [ 0.68402498960495, 0 ],
              [ 0.68402498960495, 0.9943057894706726 ],
              [ 0.06010574474930763, 0.9943057894706726 ]
          ],
          "name": "Animal",
          "score": 0.7435145974159241
      }
  ]
  ```
</details>

## Image cropping (GCloud Version)
Best shot suggestion via Google Cloud.

#### Input:
Address: `/crop-gcloud`, POST \
MIMEs: `applcation/json` \
`image/jpeg`, `image/png` -- 3/4 aspect ratio only

Parameters when json: \
`data`: base64-encoded image \
`ratio`: resulting image aspect ratio, float or (a/b)-like \
`type`: optional, image extension. Can be omitted for most of extensions.

#### Output:
List of suggested crops. \
For each crop: \
`score`:  quality [0, 1] \
`crop`: 4-element list of crop coordinates, clockwise, starting from the top left corner. <b> Coordinates are global. </b> 

<details>
  <summary> <b>Sample: </b> </summary> 

  Request JSON:
  ```json
  {
      "data": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxM...",
      "type": "jpg",
      "aspect_ratio": "3/4"
  }
  ```
  
  Response:
  ```json
  [
      {
          "crop": [
              [ 135, 0 ],
              [ 261, 0 ],
              [ 261, 167 ],
              [ 135, 167 ]
          ],
          "score": 0.45851942896842957
      }
  ]
  ```
</details>



## Image-cropping
