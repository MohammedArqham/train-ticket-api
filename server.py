import grpc
from concurrent import futures
import train_pb2
import train_pb2_grpc

class TrainTicketService(train_pb2_grpc.TrainTicketServicer):
    def __init__(self):
        self.tickets = {}
        self.user_seats = {}

    def PurchaseTicket(self, request, context):
        ticket_id = len(self.tickets) + 1
        receipt = f"Receipt #{ticket_id}: {request.user_first_name} {request.user_last_name}, From {request.departure} to {request.to}, Price: $20"
        self.tickets[ticket_id] = receipt

        seat = f"{len(self.user_seats) + 1}"
        section = "A" if len(self.user_seats) % 2 == 0 else "B"
        self.user_seats[request.user_email] = {"section": section, "seat": seat}

        return train_pb2.TicketResponse(receipt=receipt)


    def GetReceiptDetails(self, request, context):
        return train_pb2.ReceiptDetailsResponse(details=self.tickets.get(int(request.receipt), "Receipt not found"))

    def GetUserSeats(self, request, context):
        section = request.section.upper()
        users_in_section = [{"user_email": email, "section": data["section"], "seat": data["seat"]} 
                            for email, data in self.user_seats.items() if data["section"] == section]
        return train_pb2.UserSeatsResponse(user_seats=users_in_section)

    def RemoveUser(self, request, context):
        if request.user_email in self.user_seats:
            del self.user_seats[request.user_email]
            return train_pb2.RemoveUserResponse(success=True)
        else:
            return train_pb2.RemoveUserResponse(success=False)

    def ModifyUserSeat(self, request, context):
        if request.user_email in self.user_seats:
            self.user_seats[request.user_email]["section"] = request.new_section.upper()
            return train_pb2.ModifyUserSeatResponse(success=True)
        else:
            return train_pb2.ModifyUserSeatResponse(success=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    train_pb2_grpc.add_TrainTicketServicer_to_server(TrainTicketService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
