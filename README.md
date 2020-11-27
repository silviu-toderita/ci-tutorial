# CI/CD Tutorial

This repository contains everything you need to deploy a simple example that can demonstrate the benefits of continous deployment.

By the end of this tutorial, you should have a website with an AWS Lambda-powered backend that executes short functions and returns its outputs. You'll leverage a continuous deployment pipeline to test and push changes to your backend.

- [CI/CD Tutorial](#cicd-tutorial)
  - [Pre-requisites](#pre-requisites)
- [The Guts](#the-guts)
  - [Deployment](#deployment)
    - [CloudFormation](#cloudformation)
    - [Repository Configuration](#repository-configuration)
      - [Repository Settings](#repository-settings)
      - [GitHub Actions](#github-actions)
      - [GitHub Pages](#github-pages)
    - [Local Environment Setup](#local-environment-setup)
  - [Fix Existing Code](#fix-existing-code)
  - [Add Some Capabilities](#add-some-capabilities)
  - [Cleanup](#cleanup)
  - [Going Forward](#going-forward)
- [Appendix](#appendix)
    - [Cloudformation Deployment](#cloudformation-deployment)
    - [CORS](#cors)
    - [GitHub Actions](#github-actions-1)

## Pre-requisites

- An active AWS account
- GitHub Actions minutes <sup>1</sup>
- Basic Python knowledge
- Basic Git knowledge <sup>2</sup>

Some steps may assume basic knowledge of the requirements above; if you get stuck at any point, feel free to send me a message.

<sup>1</sup> You can check your remaining amount under your [billing settings](https://github.com/settings/billing)  
<sup>2</sup> I hosted a tutorial for Git [here](https://github.com/lcfyi/git-practice), if you're curious

# The Guts

The tutorial will be broken down into 3 parts: infrastructure deployment and setup, fixing existing code, and adding a new feature. Don't worry if you get stuck, hints will be available at each step that will guide you through.
## Deployment

Traditionally, infrastructure is a large part of getting continuous deployment to work smoothly. However, for simplicity and time, we'll abstract a lot of this by deploying a pre-made template using AWS CloudFormation.

CloudFormation is a service AWS offers that helps you deploy a collection of related AWS resources in a consistent and reproducible way. It takes away a lot of the guesswork and human error when deploying infrastructure, which is why we'll be using it today. For an in-depth discussion of what we're actually deploying, refer to the appendix.

**Note that everything we're deploying falls under the free-tier usage, so you shouldn't have to worry about any charges.**

### CloudFormation

Let's synthesize our resources using the template provided in this repository.

1. Navigate to your AWS console and find the AWS CloudFormation service (you can search for it)
2. Click on `Create stack`
3. Under `Prerequisite - Prepare template`, select `Template is ready` (which should be the default)
4. Under `Specify template`, select `Upload a template file`. Use the template from [here](/deployment/deployment.yaml) and plug it into CloudFormation then press `next`.
5. Give your stack a name. It doesn't matter what it is; I named mine `ci-tutorial`
6. Keep all your settings as default and keep pressing `next` until you reach the last page.
7. Under `Capabilities`, check the box that says `I acknowledge that AWS CloudFormation might create IAM resources.`
8. Click on `Create stack`

CloudFormation will now create all the resources you need, which may take a couple minutes. When the status of the deployment is `CREATE_COMPLETE` (it may not update live, refresh the page occasionally), you're ready for the next step.

### Repository Configuration

With our resources generated, we'll need to manually configure our repository with some settings, then enable GitHub Actions and GitHub Pages.

#### Repository Settings

First, let's gather the information we need to configure the repository. The secrets we'll need to configure are `AWS_REGION`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `API_URL`.

First get our region.

1. At the top right of your console, you should see three dropdowns: your username, a location, and support. Click on the location.
2. A dropdown should show up, with a region highlighted. For example, if your region was Ohio, you should see `US East (Ohio) us-east-2` highlighted.
3. Note down the region somewhere, as this will be our `AWS_REGION`. In my example, we'll write down `us-east-2`.

Next, let's generate an access key ID and secret access key.

1. Within your AWS console, navigate to IAM.
2. Under `Access management`, visit `Users` 
3. You should see a new user, starting with a name starting with what you gave your CloudFormation stack. For example, my user is `ci-tutorial-GithubActionIamUser-<UUID>`. Click on that user.
4. Click on the `Security credentials` tab, and generate a new access key by clicking on the `Create access key` button.
5. A new modal should pop up with an `Access key ID` and a `Secret access key`. Copy both of these down somewhere, as these will be our `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, respectively.

Finally, let's get our API URL.

1. Within your AWS console, navigate to API Gateway.
2. You should see a new API, which will be named what we gave our CloudFormation stack. For example, if you named the stack `ci-tutorial`, you should see a new API under `ci-tutorial`. Click on it.
3. On the left sidebar, click on `Stages`, which should show a new list with a single stage titled `api`. Click on `api`.
4. At the top of the page, you should see an `Invoke URL`.
5. Before saving that URL, add `/gateway` to the end of it. So for example, if your API URL was `https://id.execute-api.us-east-2.amazonaws.com/api`, then we'll save `https://id.execute-api.us-east-2.amazonaws.com/api/gateway`. Copy this down somewhere, as this will be our `API_URL`.

At this point, we should have our region, access key ID, secret access key, and API URL. Let's navigate back to the GitHub repository and configure some secrets.

1. Navigate to the `Settings` tab in your repository.
2. On the left, click on the `Secrets` option.
3. Click on the `New repository secret` button on the top right.
4. At this point, we'll need to add each of our secrets one by one. The four secrets we need are: `API_URL`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION`. Give the secrets those titles and put its corresponding value in the textbox.

#### GitHub Actions

This repository is already configured for GitHub actions. However, they're disabled by default for forked repositories. We just have to enable them. 

1. Navigate to the `Actions` tab in your repository.
2. Click on `I understand my workflows, go ahead and enable them`.

After enabling the actions, new pushes should trigger the workflow. Let's make an empty commit.

```sh
git commit --allow-empty -m "Empty commit to trigger workflow."
```

Now give it a couple minutes to run the workflows. There are two included: one that automatically builds our lambda functions, and another that builds our GitHub Pages frontend. Let the latter run and finish before moving onto the next step.

#### GitHub Pages

The workflow should've generated a new branch called `gh-pages`. This step deploys that branch.

1. Navigate to the `Settings` tab in your repository.
2. Scroll down to the `GitHub Pages` section.
3. Under `Source`, click on the dropdown and select the `gh-pages` branch, keep the directory as `/ (root)`, then click `Save`.

The deployment should take a couple minutes, but after it's done you should now be able to visit the frontend under `https://<your-github-username>.github.io/ci-tutorial`.

**NOTE**: it may take a while for the front-end to appear. Don't worry, it'll show up eventually.

### Local Environment Setup

Now we're going to install some dependencies locally so that we can work through the rest of the tutorial smoothly. In your terminal, type:

```bash
pip3 install -r backend/requirements.txt
```

Depending on how the rest of your environment is set up, you may not be able to run `pip3` directly. Try the following:

```bash
python3 -m pip install -r backend/requirements.txt
```

If you've made it this far then pat yourself on the back; the hard part is over.
## Fix Existing Code

So far, we've trusted that our pipeline will only deploy code that isn't broken. Let's verify this by running the test suite locally.

In your terminal, run the tests by typing in:

```sh
python3 backend/tests.py
```

What do you see? As it turns out, our test suite fails, despite our deployment succeeding. What's going on?

Let's take a closer look at our Actions definition. The file that handles the workflow for the Lambda deployment is in [`.github/workflows/lambda.yml`](./.github/workflows/lambda.yml). Open that file and examine the steps. At this point, there are 4 steps to this workflow: code checkout, dependency installation, code zip, and finally the deployment to AWS Lambda.

Clearly, we're missing a step to run our tests. Add that step and push your changes.

To get started, examine the dependency installation step and pay attention to how it runs commands. How would you get the action to run tests the same way we just did?

<details>
<summary><strong>Hint</strong></summary>
<p>

We need to add the following step to the workflow, just after the dependency installation. On line 13 of `lambda.yml`, add the following lines (keeping in mind that indentation matters).

```yml
      - name: Run Tests
        run: |
          python3 backend/tests.py
```

</p></details>

With the testing step added and pushed, your deployment should fail (and GitHub should send you emails warning you about a failed workflow). This is good, since we want our testing suite to catch our errors before deploying our code to production. Let's fix the error and push our fix. To get started, let's have a look at the failing test and examine its output. What's the issue?

Keep in mind that you can run your tests locally as much as you'd like before pushing your fix.

<details>
<summary><strong>Hint</strong></summary>
<p>

The test is failing because we're giving the `plus_one` function a non-integer value, which we expect the function to handle gracefully and return the string `Invalid input.` (as defined in the test on line 16 of `backend/tests.py`). 

To handle the error, we can simply wrap our function in a `try-except` block.

```python
def plus_one(payload):
    """Adds one to the input integer."""
    try:
        return str(int(payload) + 1)
    except ValueError:
        return "Invalid input."
```

</p></details>

At this point, your tests should pass and your changes will deploy to Lambda automatically on every push. To verify this change, visit the frontend on GitHub Pages and try a non-integer input to your function: it should now return "Invalid input." for bad inputs. The essence of this tutorial is complete here, but feel free to move on to the next step if you're feeling adventurous. Otherwise, skip ahead to cleanup.
## Add Some Capabilities

Now we're going to add a new function to our frontend dashboard.

The frontend currently polls the backend for functions that are available. In addition, the backend is configured to automatically discover new functions in `backend/routes.py` (you can see how this is done on lines 4-10 in `backend/index.py` if you're curious). The function docstring is used to describe what the function does to the frontend.

With that knowledge, let's add a new function that'll return the `n`-th fibonacci number.

To maintain the spirit of this exercise, let's write the function definition and tests first. Feel free to refer to the other functions to see how to get this set up. Here are some tests you should include (feel free to write more):

```python
fibonacci("") should return "Invalid input."
fibonacci("0") should return "0"
fibonacci("1") should return "1"
fibonacci("2") should return "1"
fibonacci("7") should return "13"
fibonacci("20") should return "6765"
```

**IMPORTANT**: the routes will receive their inputs as strings, so remember to convert it to an integer for your intermediate calculations. You should also pass in a string for your tests.

<details>
<summary><strong>Hint</strong></summary>
<p>

To get started, let's add a new function in `backend/routes.py`. At the bottom of the file, add the following function:

```python
def fibonacci(payload):
    """Computes the n-th fibonacci number."""
    return None
```

We'll implement it later.

Now let's add some tests in `backend/tests.py`. Near the bottom of the file, before `if __name__ == "__main__"`, add the following test:

```python
class FibonacciTests(unittest.TestCase):
    def test_null(self):
        self.assertEqual(fibonacci(""), "Invalid input.")

    def test_0(self):
        self.assertEqual(fibonacci("0"), "0")

    def test_1(self):
        self.assertEqual(fibonacci("1"), "1")

    def test_2(self):
        self.assertEqual(fibonacci("2"), "1")

    def test_7(self):
        self.assertEqual(fibonacci("7"), "13")

    def test_20(self):
        self.assertEqual(fibonacci("20"), "6765")
```

Run the tests:

```sh
python3 backend/tests.py
```

We should now get 6 failures.

Let's add our implementation now. Replace our function we defined earlier with the implementation below:

```python
def fibonacci(payload):
    """Computes the n-th fibonacci number."""
    try:
        payload = int(payload)
        p_0 = 0
        p_1 = 1
        for i in range(payload):
            p_0, p_1 = p_1, p_0 + p_1
        return str(p_0)
    except ValueError:
        return "Invalid input."
```

Remember, we take a string as input and require a string as output. Run the tests again, and everything should pass. 

</p></details>

Once you're done testing and implementing your fibonacci function, remember to push all your changes. After a couple minutes it should be live on your frontend and you should see a new card titled `fibonacci` (or whatever you decided to name your function). Try giving it some inputs and observing its outputs.

## Cleanup

Let's take down your AWS resources.

The great thing about CloudFormation is that it makes cleanup exceedingly easy. Simply visit your AWS console and navigate to CloudFormation. Select the stack we created in the deployment step and click on the `Delete` button. That's it.

Optionally, you can also disable the GitHub Actions and take down the GitHub Page. For the former, navigate to the `Actions` tab and select each workflow. For each workflow, you should see a `. . .` button that'll allow you to disable the workflow. Do this for both the Lambda and Pages workflows. Finally, delete the `gh-pages` branch and navigate to your repository settings to disable the GitHub Page.

## Going Forward

Hopefully these exercises gave you a new appreciation on the benefits of continuous deployment. It's extremely useful, even for small projects, and it's worth thinking about how you can automate deployments in order to reduce your future workload as your projects evolve.

For example, I use it to build and deploy my personal website and resume. The latter is a LaTeX template, so it's useful to have a build step that I can invoke without actually having LaTeX installed on the machine I'm editing on.

If you're still curious and want to learn more, feel free to read through the appendix for some discussions about the parts I've handwaved.

# Appendix

The following section includes extra information that isn't necessary to complete this tutorial, but can be useful to enhance your understanding of what's going on.

### Cloudformation Deployment

CloudFormation is a great infrastructure-as-code service, as it provides a very robust feature set for you to deploy your AWS resources together as a stack. For this tutorial, our template generates the following resources:

- API Gateway REST API
- API Gateway Resource (that's related to your REST API)
- API Gateway CORS OPTIONS Method (for CORS support, discussed below)
- API Gateway Method (to proxy to AWS Lambda)
- API Gateway Deployment (a unit of deployment which represents all the changes you made to date)
- API Gateway Stage (callable of your API, which is associated with a deployment)
- API Gateway IAM Role (an IAM role that allows API Gateway to access Lambda)
- Lambda Function (a deployable Lambda function)
- Lambda IAM Role (a base IAM role for your Lambda function)
- Github Action IAM Managed Policy (a policy that wraps the credentials that GitHub Actions requires)
- Github Action IAM User (a user that consumes the managed policy)

While none of these are complicated on its own, there are a lot of steps involved in provisioning these resources; the reproducibility of a CloudFormation tempplate makes deployments a lot easier to perform. This can be extremely useful if you're moving infrastructure from one region to another, or you have to programmatically scale your infrastructure.

The concept is widely used in industry, and you're not limited to just CloudFormation to adopt infrastructure as code.

### CORS

In this tutorial, our backend is hosted on a different domain from the frontend. This poses a problem as your browser restricts cross-origin resources by default for your safety. In order to get around this, we enable CORS (cross-origin resource sharing) on our backend to signal to your browser that it's safe to load these resources.

You can see this implemented as an OPTIONS route in our API Gateway deployment, and as a header response from our Lambda function itself. For simplicity, we've allowed every origin with a wildcard.

In general, it's not a good idea to use a wildcard; be mindful of which origins you allow.

### GitHub Actions

Each step spawns a new runner, which is a child process from the parent that handles your deployment. This also means variables aren't persisted between steps, which can impose a challenge if you want to pass environment variables between steps. Luckily, we don't need persistence beyond the file directory so we don't have to worry about that in this tutorial.