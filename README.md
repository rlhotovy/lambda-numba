# lambda-numba
A small demo showing how to compile Numba kernels for use on AWS Lambda

## Usage
There are two main parts of this repo: the code for compiling Lambda kernels (located in `src/kernels.py`) and the lambda handler that makes use of the compiled code (essentially the whole `dist` directory). For convenience, I've included a Docker file to build a container image that is able to compile the kernels (since getting all the dependencies needed to do this installed can be a bit of a pain). Here's a rundown of how to run the demo.

### Compiling the Kernels
I assume a working knowledge of building Docker images from Dockerfiles and of running an image with a mounted volume. If you're not familiar with these concepts, I suggest checking out the [documentation](https://docs.docker.com/) provided by Docker The image built by my Dockerfile is essentially Miniconda with some extra build tools on top of it that Numba uses for compiling its functions. If you have a local installation of Numba/Numpy/gcc then you can use that instead of building the Docker container.

Once you have the container built, assuming you've named it `numba-compiler`, you'll want to run a command like
```
docker run -ti -v <absolute-path-to-this-directory>:/shared numba-compiler bash
```
Once in the container bash shell, run `cd /shared/src` and run `python kernels.py`. This will create an `so` file called `kernels.so` in the `dist` folder that contains the compiled Numba kernels that can be imported into your Python code. My sample code contains two demo functions: `square` and `squarearr`, which take a number and an array of numbers (respectively) and return their squares (value-by-value for the array). You can test if this worked by changing into the `dist` directory, opening a Python shell and running something like `import kernels` and `print kernels.square(2.0)`. If this works without error, you should be good to go.

### Running in Lambda
Once you've compiled the kernels, you'll be able to run them in Lambda. To do this, create a [deployment package](http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html) using the contents of the `dist` directory. I've included a Numpy package that will run correctly on Amazon Linux (to do this, I used the [lambdalinux](https://github.com/lambda-linux/baseimage-amzn/) base image, which is also a great way of testing if your code will work in Lambda without creating an actual function). Your deployment package should look something like:
```
-- package.zip
  -- numpy/
  -- numpy-info
  -- kernels.so
  -- lambda_handler.py
```
Make sure your Lambda function defines the entry point as `lambda_handler.run_demo`, and upload the zip file as the package (or throw in on S3 and reference it there) and you should be good to go. The code should output the results of calling `square` and `squarearr` as the results of the function call.
