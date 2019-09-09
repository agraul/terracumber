# Terracumber

When [Terraform](https://www.terraform.io/) meets [Cucumber](https://cucumber.io/).

This exactly what [Uyuni](https://www.uyuni-project.org/) and [SUSE Manager](https://www.suse.com/products/suse-manager/) are you using for part of the testing. We create an environment with terraform (sumaform) and then we run tests with Cucumber.

Until [SUSE's Hackweek 18](https://hackweek.suse.com/projects/terracumber-python-replacement-for-sumaform-test-runner) we were using a set of bash scripts, completely ad-hoc and hard to maintain and extend, and that is how Terracumber as born.

# Does this only work with sumaform?

No. It should work with any other environment as long as:

1. It is created with terraform.
2. It has a controller instance (defined as root.ct.controller at terraform) to run the cucumber testsuite.
3. The cucumber run produces the following outputs: `cucumber_report`, `results_junit`, `screenshots` (as such outputs are to be published) **[1]**

**[1]** We hope to make this configurable in the future.

# How should I use it?

## Software requirements

- Python3
- Terraform installed and configured as need to run the terrafrom teplates you are going to use

## Create/adjust your .tf file

You will need to create at least one `.tf` file to use it to launch your environment, as well as configuring everything else (such as what command to run for the testsuite).

Keep in mind:
1. There are some mandatory variables that the `.tf` file (see one of the [examples](examples/)
2. You can add extra variables to your `.tf` file, so you can use it when creating the environment. Those variables will need to be exported before running `terraform-cli` as `TF_VAR_`, as explained at the [terraform doc](https://learn.hashicorp.com/terraform/getting-started/variables.html#from-environment-variables). Our example adds SCC credentials to pass them to Uyuni/SUSE Manager, and GitHub credentials to use them to clone the GitHub cucumber repository **[1]**

**[1]** To clone your terraform repository, it is allowed to use `TF_VAR_GIT_USER` and `TF_VAR_GIT_USER` instead of `--gituser` and `--gitpassword`, in case you do not want the credentials visible at the list of processes. If you use both the environment and the variables, then the parameters will be used to clone the terraform repository, and the variables to clone the cucumber repository at the controller.

## Create email templates

You need to create two email templates, one to be used when the environment fails to be created, the other to be used after cucumber is able to run.

The email templates are plain text files with some variables to be replaced by `terraform-cli`:

* `$urlprefix` - Directly from your `.tf` file, from variable `URL_PREFIX`
* `$timestamp` - Either the environment variable `BUILD_NUMBER` provided by Jenkins, or a timestamp in format `%Y-%m-%d-%H-%M-%S` otherwise (corresponding to the time and date when `terraform-cli` started.
* `$tests` - Total number of tests executred by cucumber
* `$passed` - Number of tests executed by cucumber without failures or erorrs
* `$failures` - Number of tests executed by cucumber with failures
* `$errors` - Number of tests executed by cucumber with errors
* `$skipped` - Number of tests skipped by cucumber
* `$failures_log` - A list of failed tests, the number of failures is determined by `terraform-cli` `--nlines` parameter

# Bonus: clean old results

The script `clean-results` can be used to get rid of undesired old results (use `-h` to get help) 