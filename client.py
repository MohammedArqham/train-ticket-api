import grpc
import train_pb2
import train_pb2_grpc

def purchase_ticket(stub):
    request = train_pb2.TicketRequest(
        departure="London",
        to="France",
        user_first_name="John",
        user_last_name="Doe",
        user_email="john.doe@example.com",
    )
    response = stub.PurchaseTicket(request)
    print(f"Purchase Ticket Response:\n{response.receipt}")

def get_receipt_details(stub, receipt):
    request = train_pb2.ReceiptDetailsRequest(receipt=str(receipt))
    response = stub.GetReceiptDetails(request)
    print(f"Receipt Details Response:\n{response.details}")

def view_user_seats(stub):
    request = train_pb2.UserSeatsRequest(section="A")
    response = stub.GetUserSeats(request)
    print(f"User Seats in Section A:\n{response.user_seats}")


def get_user_seats(stub, section):
    request = train_pb2.UserSeatsRequest(section=section)
    response = stub.GetUserSeats(request)
    print(f"User Seats in Section {section}:\n{response.user_seats}")

def remove_user(stub, user_email):
    request = train_pb2.RemoveUserRequest(user_email=user_email)
    response = stub.RemoveUser(request)
    if response.success:
        print(f"User {user_email} removed successfully.")
    else:
        print(f"User {user_email} not found.")

def modify_user_seat(stub, user_email, new_section):
    request = train_pb2.ModifyUserSeatRequest(user_email=user_email, new_section=new_section)
    response = stub.ModifyUserSeat(request)
    if response.success:
        print(f"User {user_email} seat modified to Section {new_section} successfully.")
    else:
        print(f"User {user_email} not found.")



def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = train_pb2_grpc.TrainTicketStub(channel)
        purchase_ticket(stub)
        get_receipt_details(stub, receipt=1)
        view_user_seats(stub)  
        remove_user(stub, "john.doe@example.com")
        view_user_seats(stub)

if __name__ == '__main__':
    run()



