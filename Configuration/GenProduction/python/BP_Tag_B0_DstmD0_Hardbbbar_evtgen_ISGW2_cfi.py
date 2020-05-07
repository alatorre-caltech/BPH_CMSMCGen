import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            operates_on_particles = cms.vint32(511),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
#
# This is the decay file for the decay B0 -> Dst Hc (-> mu)
#
yesPhotos
#
Alias myLepD0 D0
Decay myLepD0
0.03410     K-      mu+     nu_mu                           PHOTOS  ISGW2; # PDG2019
0.01890     K*-     mu+     nu_mu                           PHOTOS  ISGW2; # PDG2019
0.00260     pi-     mu+     nu_mu                           PHOTOS  ISGW2; # PDG2019
0.00177     rho-    mu+     nu_mu                           PHOTOS  ISGW2; # PDG2019 for electron
Enddecay
# Inclusive Br from PDG2020 D0 -> mu +X = 6.8 +/- 0.6%
#
Alias myLepD*0 D*0
Decay myLepD*0
0.61900     myLepD0      pi0                                VSS; #[Reconstructed PDG2011]
0.38100     myLepD0      gamma                              VSP_PWAVE; #[Reconstructed PDG2011]
Enddecay
#
Alias myLepD*+ D*+
Decay myLepD*+
0.67700     myLepD0  pi+                                    VSS;
Enddecay
#
#
#
#
#
##########################################
#           D*- -> D0(->Kpi) pi
##########################################
#
Alias      Myanti-D0   anti-D0
Decay Myanti-D0
1.000      K+  pi-                PHSP;
Enddecay
#
Alias     MyD*-    D*-
Decay MyD*-
1.000      Myanti-D0 pi-          VSS;
Enddecay
#
#
#
#
#
#
#
##########################################
#           B0 -> D*- D0
##########################################
#
Decay B0
0.00250     MyD*-         myLepD0         K+                        PHSP; # [Reconstructed PDG2020]
0.00500     MyD*-         myLepD0         K*+                       PHSP; # Not reported in PDG, given a reasonable value
0.01060     MyD*-         myLepD*0        K+                        PHSP; # [Reconstructed PDG2020]
0.00500     MyD*-         myLepD*0        K*+                       PHSP; # Not reported in PDG, given a reasonable value
0.00550     MyD*-         myLepD*+        K0                        PHSP; # [Reconstructed PDG2020]   #  0.00810*0.67700 = 0.00550 (not all D*+ -> D0)
0.00370     MyD*-         myLepD*+        K*0                       PHSP; # Not reported in PDG, given a reasonable value. 0.0050*0.677 = 0.0037
Enddecay
End
"""
                                            )
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring('HardQCD:hardbbbar = on'),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)


###### Filters ##########
mufilter = cms.EDFilter("PythiaFilter",
    MaxEta     = cms.untracked.double(1.6),
    MinEta     = cms.untracked.double(-1.6),
    MinPt      = cms.untracked.double(6.7),
    ParticleID = cms.untracked.int32(13),
    MotherID   = cms.untracked.int32(421) # D0
)

DstFilter = cms.EDFilter(
    "PythiaDauVFilter",
    ParticleID         = cms.untracked.int32(-413),
    MotherID           = cms.untracked.int32(511),
    ChargeConjugation  = cms.untracked.bool(False),
    NumberDaughters    = cms.untracked.int32(2),
    DaughterIDs        = cms.untracked.vint32(-421, -211),
    MinPt              = cms.untracked.vdouble(0.5, 0.3),
    MinEta             = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta             = cms.untracked.vdouble( 2.5, 2.5)
)

antiD0Filter = cms.EDFilter(
    "PythiaDauVFilter",
    ChargeConjugation  = cms.untracked.bool(False),
    ParticleID         = cms.untracked.int32(-421),
    MotherID           = cms.untracked.int32(-413),
    NumberDaughters    = cms.untracked.int32(2),
    DaughterIDs        = cms.untracked.vint32(321, -211),
    MinPt              = cms.untracked.vdouble(0.5, 0.5),
    MinEta             = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta             = cms.untracked.vdouble( 2.5, 2.5)
)

ProductionFilterSequence = cms.Sequence(generator + mufilter + DstFilter + antiD0Filter)
