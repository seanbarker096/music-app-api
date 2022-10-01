from os import getenv


def initialize_flask_server_debugger_if_needed():
    if getenv("DEBUGGER") == "True":
        import multiprocessing

        print("test")
        if multiprocessing.current_process().pid > 1:
            import debugpy

            print("test2", flush=True)
            debugpy.listen(
                ("0.0.0.0", 10001)
            )  # This will start the debug adapter that will listen for a client connection at the 0.0.0.0:10001 interface.
            print("⏳ VS Code debugger can now be attached, press F5 in VS Code ⏳", flush=True)
            ## Might want to remove this as it reuqires f5 to be hit whenever code change is made for hot reload to update code
            debugpy.wait_for_client()  # This line will block program execution until a client (in our case, the client will be the VS Code debugger) is attached.
            print("🎉 VS Code debugger attached, enjoy debugging 🎉", flush=True)
