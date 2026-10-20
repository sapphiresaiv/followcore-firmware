# Safety

These release candidates are for controlled evaluation. They are not a
safety-certified controller, STO implementation, or guarantee against damage.

Keep the mechanism clear, assess gravity/load hazards, and provide appropriate
independent emergency-stop and mechanical protection. Software stop, CAN
supervision, homing detection, and current observations do not replace them.

Do not test repeated end-stop contact unattended. Homing repeatability, contact
force, operating limits, loaded response, and worst-case communication timing
require qualification on the actual machine. A measured current is not a
universal safe-force specification for a screw mechanism.

Updates reset control state and can invalidate the homing reference. Do not
update while relying on motor holding torque to support an unsecured load.
Firmware must not automatically resume motion after updating, fault recovery,
or a broken communication session.
