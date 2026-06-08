'''
To run the script
- Start the AWS Academy Learner Lab

On the Vocareum window
- Click on "Start lab"
- Click on "AWS Details"
- Click on "ASW CLI: Show"
- Copy the contet of the displayed window

In the termianl / PowerShell of your computer
- Paste the content of the displayed widown to ~/.aws/credentials as follows:
  - mkdir ~/.aws
  - cat > ~/.aws/credentials
  (paste the content and hit a return key)
  CTRL+D (press CTRL and D keys together)
- Run this Python script
  - python skills_lab_1_assessment.py  or  python3 skills_lab_1_assessment.py
  Or 
  - load this script in VS Code and run it
- Run this Pythong script and direcct the output to both the screen and a file
  On bash
    - python skills_lab_1_assessment.py | tee output.txt
  On PowerShell
    - python script.py | Tee-Object -FilePath "output.txt"

'''


import subprocess
import json
from rich import print

# Debug switch
DEBUG_MODE = False

# parameters to check
VPC_NAME = "lab1-vpc"
IGW_NAME = "lab1-igw"
NGW_NAME = "lab1-nat-public1-us-east-1"
PUB_SUBNET_NAME = "lab1-subnet-public1-us-east-1*"
PUB_SUBNET_CIDR = "10.10.0.0/20"
PRI_SUBNET_NAME = "lab1-subnet-private1-us-east-1*"
PRI_SUBNET_CIDR = "10.10.128.0/20"
PUB_RT_NAME = "lab1-rtb-public"
PRI_RT_NAME = "lab1-rtb-private1-us-east-1"

# each test is worth 4 points by default
# adjust this value in each test as needed
SCORE = 4
total_score = 0

# debug message
def log(message):
    if DEBUG_MODE:
        print(f"    [yellow][DEBUG][/] {message}")

def test_1():
    #
    # Test 1
    # See if VPC (lab1_vpc) exists
    #
    test_id = "1.0"
    test_name = "Does VPC (lab1-vpc) exist?"
    global total_score
    search_filter = f"*{VPC_NAME.strip()}*"
    vpc_id = "null"
    try:
        result = subprocess.run([
            "aws", "ec2", "describe-vpcs", 
            "--filters", f"Name=tag:Name,Values={search_filter}", 
            "--query", "Vpcs[0].VpcId", 
            "--output", "json"
                ], capture_output=True, text=True, check=True) 

        vpc_id = json.loads(result.stdout.strip())
        log(f"{test_id}: vpc_id {vpc_id}")

        if vpc_id and vpc_id not in ["None", "null", ""]:
            total_score += SCORE
            print(f"[green]Passed[/]: {test_id}: {test_name}, +{SCORE}")
            log(f"{VPC_NAME} is found at {vpc_id}")
        else:
            print(f"[red]Failed[/]: {test_id}: {test_name}")

    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e.stderr.strip()}")
        print(f"[red]Failed[/]: {test_id}: {test_name}")

    return vpc_id

def test_2(vpc_id):
    #
    # Test 2
    # Internet Gateway
    #

    #
    # Test 2.1
    # See if Internet Gateway (lab1-igw) exists

    test_id = "2.1"
    test_name = "Does Internet Gateway (lab1-igw) exist?"
    global total_score
    search_filter = f"*{IGW_NAME.strip()}*"
    igw_id = "null"

    log(f"{test_id}: vpc_id {vpc_id}")

    if vpc_id in ["None", "null", ""]:
        print(f"[red]Failed[/]: {test_id}: {test_name}")
        log(f"{VPC_NAME} does not exist, so {IGW_NAME} cannot exist")
        return igw_id

    try:
        result = subprocess.run([
            "aws", "ec2", "describe-internet-gateways",
            "--filters", f"Name=tag:Name,Values={search_filter}",
            "--query", "InternetGateways[0].InternetGatewayId",
            "--output", "json"
        ], capture_output=True, text=True, check=True) 

        igw_id = json.loads(result.stdout.strip())
        log(f"{test_id}: igw_id {igw_id}")

        if igw_id and igw_id not in ["None", "null", ""]:
            total_score += SCORE - 2
            print(f"[green]Passed[/]: {test_id}: {test_name},  +{SCORE - 2}")
            # log(f"{IGW_NAME} is found at {igw_id}")
        else:
            print(f"[red]Failed[/]: {test_id}: {test_name}")

    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e.stderr.strip()}")
        print(f"[red]Failed[/]: {test_id}: {test_name}")

    #
    # Test 2.2
    # See if Internet Gateway (lab1-igw) is attached to PVC (lab1-vpc)
    #
    test_id = "2.2"
    test_name = "Is lab1-igw associated with lab1-vpc?"
    search_filter = f"*{IGW_NAME.strip()}*"
    
    try:
        result = subprocess.run([
            "aws", "ec2", "describe-internet-gateways",
            "--filters", f"Name=tag:Name,Values={search_filter}",
            "--query", "InternetGateways[0].Attachments[0].VpcId",
            "--output", "json"
        ], capture_output=True, text=True)

        vpc_id_returned = json.loads(result.stdout.strip())
        log(f"{test_id}: vpc_id_returned {vpc_id_returned}")

        if vpc_id_returned == vpc_id:

            total_score += SCORE - 2
            print(f"[green]Passed[/]: {test_id}: {test_name}, +{SCORE - 2}")
            # log(f"{igw_id} is assocaited with {vpc_id}")
        elif igw_id in ["None", "null", ""]:
            print(f"[red]Failed[/]: {test_id}: {test_name}")
            log(f"{igw_id} exists but is NOT assocaited with any VPC")
        else:
            print(f"[red]Failed[/]: {test_id}: {test_name}")
            log(f"{igw_id} exists but is NOT assocaited with {vpc_id}")

    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e.stderr.strip()}")
        print(f"[red]Failed[/]: {test_id}: {test_name}")

    return igw_id

def test_3(vpc_id):
    #
    # Test 3
    # See if NAT Gatway (lab1-natgw) exists
    #
    test_id = "3.0"
    test_name = "Does NAT Gatway (lab1-natgw) exist?"
    global total_score
    search_filter = f"*{NGW_NAME.strip()}*"
    ngw_id = "null"

    try:
        result = subprocess.run([
            "aws", "ec2", "describe-nat-gateways",
            "--filter", f"Name=tag:Name,Values={search_filter}",
            "--query", "NatGateways[0].{ID:NatGatewayId,State:State}",
            "--output", "json"
        ], capture_output=True, text=True, check=True) 

        output = json.loads(result.stdout.strip())
        log(f"{test_id}: {output}")

        if output and output not in ["None", "null", ""]:
            ngw_id = output['ID']
            total_score += SCORE
            print(f"[green]Passed[/]: {test_id}: {test_name}, +{SCORE}")
            log(f"{NGW_NAME} is found at {ngw_id}")
        else:
            print(f"[red]Failed[/]: {test_id}: {test_name} (NAT Gateway not found)")

    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e.stderr.strip()}")
        print(f"[red]Failed[/]: {test_id}: {test_name}")

    return ngw_id

def test_4(vpc_id):
    #
    # Test 4
    # Subnets
    #

    #
    # Test 4.1
    # See if Public subnet (lab1-subnet-public1-us-east-1) exists
    #
    test_id = "4.1"
    test_name = "Does public subnet (lab1-subnet-public1-us-east-1) exist?"
    global total_score 
    search_filter = f"*{PUB_SUBNET_NAME.strip()}*"
    pub_subnet_id = "null"
    pri_subnet_id = "null"
    sub_test_id = 0

    try:
        result = subprocess.run([
            "aws", "ec2", "describe-subnets",
            "--filters", f"Name=tag:Name,Values={search_filter}",
            "--query", "Subnets[0].{ID:SubnetId,VPC:VpcId,CIDR:CidrBlock}",
            "--output", "json"
        ], capture_output=True, text=True, check=True)

        output = json.loads(result.stdout.strip())
        log(f"{test_id}: {output}")

        if output and output not in ["None", "null", ""]:
            pub_subnet_id = output['ID']
            vpc_id_returned = output['VPC']
            pub_subnet_cidr_returned = output['CIDR']

            if vpc_id_returned == vpc_id:
                if pub_subnet_cidr_returned == PUB_SUBNET_CIDR:

                    total_score += SCORE - 2
                    print(f"[green]Passed[/]: {test_id}: {test_name}, +{SCORE - 2}")
                    log(f"{PUB_SUBNET_NAME} ({pub_subnet_id}) is found in "
                        f"{VPC_NAME} ({vpc_id}) with {PUB_SUBNET_CIDR}")

                else:
                    print(f"[red]Failed[/]: {test_id}: {test_name}")
                    print(f"ERROR: Public subnet has a wrong CIDR block "
                        f"{pub_subnet_cidr_returned}! "
                        f"Expected {PUB_SUBNET_CIDR}" )

            else:
                print(f"[red]Failed[/]: {test_id}: {test_name}")
                print(f"ERROR: Public subnet is in a wrong VPC {vpc_id_returned}! "
                    f"Expected {vpc_id}")
        else:
            print(f"[red]Failed[/]: {test_id}: {test_name}")
            print(f"ERROR: {PUB_SUBNET_NAME} is not found.")

    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e.stderr.strip()}")
        print(f"[red]Failed[/]: {test_id}: {test_name}")

    #
    # Test 4.2
    # See if Private subnet (lab1-subnet-private1-us-east-1) exists
    #
    test_id = "4.2"
    test_name = "Does private subnet (lab1-subnet-private1-us-east-1) exist?"
    search_filter = f"*{PRI_SUBNET_NAME.strip()}*"

    try:
        result = subprocess.run([
            "aws", "ec2", "describe-subnets",
            "--filter", f"Name=tag:Name,Values={search_filter}",
            "--query", "Subnets[0].{ID:SubnetId,VPC:VpcId,CIDR:CidrBlock}",
            "--output", "json"
        ], capture_output=True, text=True, check=True)

        output = json.loads(result.stdout.strip())
        log(f"{test_id}: {output}")

        if output and output not in ["None", "null", ""]:
            pri_subnet_id = output['ID']
            vpc_id_returned = output['VPC']
            pri_subnet_cidr_returned = output['CIDR']

            if vpc_id_returned == vpc_id:
                if pri_subnet_cidr_returned == PRI_SUBNET_CIDR:

                    total_score += SCORE - 2
                    print(f"[green]Passed[/]: {test_id}: {test_name}, +{SCORE - 2}")
                    log(f"{PRI_SUBNET_NAME} ({pri_subnet_id}) is found in "
                        f"{VPC_NAME} ({vpc_id}) with {PRI_SUBNET_CIDR}")

                else:
                    print(f"[red]Failed[/]: {test_id}: {test_name}")
                    print(f"ERROR: Private subnet has a wrong CIDR block "
                        f"{pri_subnet_cidr_returned}! "
                        f"Expected {PRI_SUBNET_CIDR}" )

            else:
                print(f"[red]Failed[/]: {test_id}: {test_name}")
                print(f"ERROR: Private subnet is in a wrong VPC {vpc_id_returned}! "
                    f"Expected {vpc_id}")
        else:
            print(f"[red]Failed[/]: {test_id}: {test_name}")
            print(f"ERROR: {PRI_SUBNET_NAME} is not found.")

    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e.stderr.strip()}")
        print(f"[red]Failed[/]: {test_id}: {test_name}")
    
    return pub_subnet_id, pri_subnet_id

def test_5(pub_subnet_id, pri_subnet_id, igw_id, ngw_id):
    #
    # Test 5
    # Route tables
    #

    # 
    # Test 5.1 
    # See if public route table (lab1-rtb-public) exists
    #
    test_id = "5.1"
    test_name = "Does public route table (lab1-rtb-public) exist?"
    search_filter = f"*{PUB_RT_NAME.strip()}*"
    global total_score 
    pub_rt_id = "null"
    pri_rt_id = "null"
    log(f"{test_id}: pub_subnet_id: {pub_subnet_id}, pri_subnet_id: {pri_subnet_id}, igw_id: {igw_id}, ngw_id: {ngw_id}")

    try:
        if pub_subnet_id in ["None", "null", ""]:
            raise subprocess.CalledProcessError(
                returncode=1, 
                cmd="pub_subnet_id does not exist",
                stderr="Public subnet ID missing or invalid"
            )

        result = subprocess.run([
            "aws", "ec2", "describe-route-tables",
            "--filters", f"Name=tag:Name,Values={search_filter}",
            "--query", "RouteTables[0].Associations[*].{rt_id:RouteTableId,subnet_id:SubnetId}",
            "--output", "json"
        ], capture_output=True, text=True, check=True)

        output = json.loads(result.stdout.strip())
        log(f"{test_id}: {output}")

        if output and output not in ["None", "null", ""]:

            route = next((route for route in output \
                if route.get("subnet_id") == pub_subnet_id), None)

            log(f"{test_id}: {route}")
            if route and route not in ["None", "null", ""]:

                pub_rt_id = route.get('rt_id')
                subnet_id_returned = route.get('subnet_id')

                if subnet_id_returned == pub_subnet_id:

                    total_score += SCORE
                    print(f"[green]Passed[/]: {test_id}: {test_name}, +{SCORE}")
                    log(f"{PUB_RT_NAME} ({pub_rt_id}) is found in "
                        f"{PUB_SUBNET_NAME} ({pub_subnet_id})")
                else:
                    print(f"[red]Failed[/]: {test_id}: {test_name}")
                    print(f"ERROR: Public route table is not associated with the correct subnet {subnet_id_returned}. "
                        f"Expected {pub_subnet_id}")
            else:
                print(f"[red]Failed[/]: {test_id}: {test_name}")
                print(f"ERROR: {PUB_RT_NAME} exists but no route to {PUB_SUBNET_NAME} {pub_subnet_id} exists.")
        else:
            print(f"[red]Failed[/]: {test_id}: {test_name}")
            print(f"ERROR: {PUB_RT_NAME} is not found.")

    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e.stderr.strip()}")
        print(f"[red]Failed[/]: {test_id}: {test_name}")

    # 
    # Test 5.2 
    # See if public route table (lab1-rtb-public) has the route to IGW
    #
    test_id = "5.2"
    test_name = "Does public route table (lab1-rtb-public) have the route to IGW (lab1-igw)?"
    search_filter = f"*{PUB_RT_NAME.strip()}*"
    local_score = 0
    try:

        if igw_id in ["None", "null", ""]:
            raise subprocess.CalledProcessError(
                returncode=1, 
                cmd="igw_id does not exist",
                stderr="IGW ID missing or invalid"
            )

        result = subprocess.run([
            "aws", "ec2", "describe-route-tables",
            "--filters", f"Name=tag:Name,Values={search_filter}",
            # This specifically picks the GatewayId for the default route
            "--query", "RouteTables[0].Routes[*].{igw_id:GatewayId,dest_cidr:DestinationCidrBlock}",
            "--output", "json"
        ], capture_output=True, text=True, check=True)

        output = json.loads(result.stdout.strip())
        log(f"{test_id}: {output}")

        if output and output not in ["None", "null", ""]:

            igw_id_returned = next((route.get("igw_id") for route in output \
                if route.get("dest_cidr") == "0.0.0.0/0"), None)

            if igw_id_returned == igw_id:

                total_score += SCORE
                print(f"[green]Passed[/]: {test_id}: {test_name}, +{SCORE}")
                log(f"{PUB_RT_NAME} ({pub_rt_id}) has a route to "
                    f"{IGW_NAME} ({igw_id})")
            else:
                print(f"[red]Failed[/]: {test_id}: {test_name}")
                print(f"ERROR: Wrong target {igw_id_returned}! "
                    f"Expected {igw_id}")
        else:
            print(f"[red]Failed[/]: {test_id}: {test_name}")
            print(f"ERROR: {PUB_RT_NAME} is not found.")

    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e.stderr.strip()}")
        print(f"[red]Failed[/]: {test_id}: {test_name}")

    # 
    # Test 5.3 
    # See if private route table (lab1-rtb-private1-us-east-1) exists
    #
    test_id = "5.3"
    test_name = "Does private route table (lab1-rtb-private1-us-east-1) exist?"
    search_filter = f"*{PRI_RT_NAME.strip()}*"
    try:

        if pri_subnet_id in ["None", "null", ""]:
            raise subprocess.CalledProcessError(
                returncode=1, 
                cmd="pri_subnet_id does not exist",
                stderr="Private subnet ID missing or invalid"
            )

        result = subprocess.run([
            "aws", "ec2", "describe-route-tables",
            "--filters", f"Name=tag:Name,Values={search_filter}",
            # Use a filter inside the query to find the association that has a SubnetId
            "--query", "RouteTables[0].Associations[*].{rt_id:RouteTableId,subnet_id:SubnetId}",
            # "--query", "RouteTables[0].{rt_id:RouteTableId,subnet_id:SubnetId}",
            "--output", "json"
        ], capture_output=True, text=True, check=True)

        output = json.loads(result.stdout.strip())
        log(f"{test_id}: {output}")

        if output and output not in ["None", "null", ""]:

            route = next((route for route in output \
                if route.get("subnet_id") == pri_subnet_id), None)

            pri_rt_id = route['rt_id']
            subnet_id_returned = route['subnet_id']

            if subnet_id_returned == pri_subnet_id:
                total_score += SCORE
                print(f"[green]Passed[/]: {test_id}: {test_name}, +{SCORE}")
                log(f"{PRI_RT_NAME} ({pri_subnet_id}) is found in "
                    f"{PRI_SUBNET_NAME} ({pri_subnet_id})")
            else:
                print(f"[red]Failed[/]: {test_id}: {test_name}")
                print(f"ERROR: Private route table is not associated with the correct subnet {subnet_id_returned}! "
                    f"Expected {pri_subnet_id}")
        else:
            print(f"[red]Failed[/]: {test_id}: {test_name}")
            print(f"ERROR: {PRI_RT_NAME} is not found.")

    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e.stderr.strip()}")
        print(f"[red]Failed[/]: {test_id}: {test_name}")

    # 
    # Test 5.4 
    # See if private route table (lab1-rtb-private1-us-east-1) has the route to NGW
    #
    test_id = "5.4"
    test_name = "Does private route table (lab1-rtb-private1-us-east-1) have the route to NGW (lab1-nat-public1-us-east-1)?"
    search_filter = f"*{PRI_RT_NAME.strip()}*"
    local_score = 0
    try:

        if ngw_id in ["None", "null", ""]:
            raise subprocess.CalledProcessError(
                returncode=1, 
                cmd="ngw_id does not exist",
                stderr="NGW ID missing or invalid"
            )

        result = subprocess.run([
            "aws", "ec2", "describe-route-tables",
            "--filters", f"Name=tag:Name,Values={search_filter}",
            "--query", "RouteTables[0].Routes[*].{rt_ngw_id:NatGatewayId,dest_cidr:DestinationCidrBlock}",
            "--output", "json"
        ], capture_output=True, text=True, check=True)

        output = json.loads(result.stdout.strip())
        log(f"{test_id}: {output}")

        if output and output not in ["None", "null", ""]:

            ngw_id_returned = next((route.get("rt_ngw_id") for route in output \
                if route.get("dest_cidr") == "0.0.0.0/0"), None)

            if ngw_id_returned == ngw_id:
                total_score += SCORE
                print(f"[green]Passed[/]: {test_id}: {test_name}, +{SCORE}")
                log(f"{PRI_RT_NAME} ({pri_rt_id}) has a route to "
                    f"{NGW_NAME} ({ngw_id})")
            else:
                print(f"[red]Failed[/]: {test_id}: {test_name}")
                print(f"ERROR: Wrong target {ngw_id_returned}! "
                    f"Expected {ngw_id}")
        else:
            print(f"[red]Failed[/]: {test_id}: {test_name}")
            print(f"ERROR: {PRI_RT_NAME} is not found.")

    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e.stderr.strip()}")
        print(f"[red]Failed[/]: {test_id}: {test_name}")

def main():

    vpc_id = test_1()
    igw_id = test_2(vpc_id)
    ngw_id = test_3(vpc_id)
    pub_subnet_id, pri_subnet_id = test_4(vpc_id)
    test_5(pub_subnet_id, pri_subnet_id, igw_id, ngw_id)

    print(f"The total score for the auto-grading portion of the exam is {total_score} points.")

if __name__ == "__main__":
    main()